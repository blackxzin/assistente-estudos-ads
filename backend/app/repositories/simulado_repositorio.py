from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.disciplina import Disciplina
from app.models.material import Material
from app.models.questao import Questao
from app.models.resposta_simulado import RespostaSimulado
from app.models.simulado import Simulado
from app.schemas.simulado import QuestaoGerada


class SimuladoRepositorio:
    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao

    async def criar(self, material_id: int, questoes: list[QuestaoGerada]) -> Simulado:
        simulado = Simulado(material_id=material_id)
        self.sessao.add(simulado)
        await self.sessao.flush()

        for questao in questoes:
            self.sessao.add(
                Questao(
                    simulado_id=simulado.id,
                    enunciado=questao.enunciado,
                    alternativas=questao.alternativas,
                    correta=questao.correta,
                    explicacao=questao.explicacao,
                    trecho_id=questao.trecho_id,
                )
            )

        await self.sessao.commit()
        await self.sessao.refresh(simulado, attribute_names=["questoes"])
        return simulado

    async def buscar_por_id_e_usuario(self, simulado_id: int, usuario_id: int) -> Simulado | None:
        resultado = await self.sessao.execute(
            select(Simulado)
            .join(Material, Simulado.material_id == Material.id)
            .join(Disciplina, Material.disciplina_id == Disciplina.id)
            .where(Simulado.id == simulado_id, Disciplina.usuario_id == usuario_id)
            .options(selectinload(Simulado.questoes))
        )
        return resultado.scalar_one_or_none()

    async def salvar_correcao(
        self, simulado: Simulado, nota: float, respostas: list[tuple[int, int | None, bool]]
    ) -> Simulado:
        for questao_id, alternativa, acertou in respostas:
            self.sessao.add(
                RespostaSimulado(questao_id=questao_id, alternativa_escolhida=alternativa, acertou=acertou)
            )

        simulado.nota = nota
        simulado.corrigido_em = datetime.now(UTC)
        await self.sessao.commit()
        await self.sessao.refresh(simulado)
        return simulado

    async def listar_corrigidos_por_usuario(self, usuario_id: int, limite: int) -> list[tuple[Simulado, str]]:
        resultado = await self.sessao.execute(
            select(Simulado, Material.titulo)
            .join(Material, Simulado.material_id == Material.id)
            .join(Disciplina, Material.disciplina_id == Disciplina.id)
            .where(Disciplina.usuario_id == usuario_id, Simulado.nota.is_not(None))
            .order_by(Simulado.corrigido_em.desc())
            .limit(limite)
        )
        return [(linha.Simulado, linha.titulo) for linha in resultado]

    async def calcular_media_e_total_por_usuario(self, usuario_id: int) -> tuple[float | None, int]:
        resultado = await self.sessao.execute(
            select(func.avg(Simulado.nota), func.count(Simulado.id))
            .join(Material, Simulado.material_id == Material.id)
            .join(Disciplina, Material.disciplina_id == Disciplina.id)
            .where(Disciplina.usuario_id == usuario_id, Simulado.nota.is_not(None))
        )
        media, total = resultado.one()
        return (float(media) if media is not None else None), total
