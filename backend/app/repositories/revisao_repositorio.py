from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.disciplina import Disciplina
from app.models.material import Material
from app.models.revisao import Revisao, StatusRevisao


class RevisaoRepositorio:
    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao

    async def criar(self, material_id: int, data_prevista: date, etapa: int) -> Revisao:
        revisao = Revisao(material_id=material_id, data_prevista=data_prevista, etapa=etapa)
        self.sessao.add(revisao)
        await self.sessao.commit()
        await self.sessao.refresh(revisao)
        return revisao

    async def buscar_por_id_e_usuario(self, revisao_id: int, usuario_id: int) -> Revisao | None:
        resultado = await self.sessao.execute(
            select(Revisao)
            .join(Material, Revisao.material_id == Material.id)
            .join(Disciplina, Material.disciplina_id == Disciplina.id)
            .where(Revisao.id == revisao_id, Disciplina.usuario_id == usuario_id)
        )
        return resultado.scalar_one_or_none()

    async def listar_pendentes_por_disciplina(self, disciplina_id: int) -> list[Revisao]:
        resultado = await self.sessao.execute(
            select(Revisao)
            .join(Material, Revisao.material_id == Material.id)
            .where(Material.disciplina_id == disciplina_id, Revisao.status == StatusRevisao.PENDENTE)
        )
        return list(resultado.scalars().all())

    async def listar_por_usuario_no_periodo(
        self, usuario_id: int, de: date, ate: date
    ) -> list[tuple[Revisao, str, str]]:
        resultado = await self.sessao.execute(
            select(Revisao, Material.titulo, Disciplina.nome)
            .join(Material, Revisao.material_id == Material.id)
            .join(Disciplina, Material.disciplina_id == Disciplina.id)
            .where(
                Disciplina.usuario_id == usuario_id,
                Revisao.data_prevista >= de,
                Revisao.data_prevista <= ate,
            )
            .order_by(Revisao.data_prevista)
        )
        return [(linha.Revisao, linha.titulo, linha.nome) for linha in resultado]

    async def listar_pendentes_de_hoje_por_usuario(self, usuario_id: int) -> list[tuple[Revisao, str, str]]:
        hoje = date.today()
        resultado = await self.sessao.execute(
            select(Revisao, Material.titulo, Disciplina.nome)
            .join(Material, Revisao.material_id == Material.id)
            .join(Disciplina, Material.disciplina_id == Disciplina.id)
            .where(
                Disciplina.usuario_id == usuario_id,
                Revisao.data_prevista == hoje,
                Revisao.status == StatusRevisao.PENDENTE,
            )
            .order_by(Revisao.id)
        )
        return [(linha.Revisao, linha.titulo, linha.nome) for linha in resultado]

    async def atualizar(self, revisao: Revisao, dados: dict) -> Revisao:
        for campo, valor in dados.items():
            setattr(revisao, campo, valor)
        await self.sessao.commit()
        await self.sessao.refresh(revisao)
        return revisao
