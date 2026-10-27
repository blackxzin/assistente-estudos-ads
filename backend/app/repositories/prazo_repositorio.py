from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.disciplina import Disciplina
from app.models.prazo import Prazo, TipoPrazo


class PrazoRepositorio:
    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao

    async def criar(self, disciplina_id: int, titulo: str, tipo: TipoPrazo, data: date) -> Prazo:
        prazo = Prazo(disciplina_id=disciplina_id, titulo=titulo, tipo=tipo, data=data)
        self.sessao.add(prazo)
        await self.sessao.commit()
        await self.sessao.refresh(prazo)
        return prazo

    async def listar_por_disciplina(self, disciplina_id: int) -> list[Prazo]:
        resultado = await self.sessao.execute(select(Prazo).where(Prazo.disciplina_id == disciplina_id))
        return list(resultado.scalars().all())

    async def buscar_por_id_e_usuario(self, prazo_id: int, usuario_id: int) -> Prazo | None:
        resultado = await self.sessao.execute(
            select(Prazo)
            .join(Disciplina, Prazo.disciplina_id == Disciplina.id)
            .where(Prazo.id == prazo_id, Disciplina.usuario_id == usuario_id)
        )
        return resultado.scalar_one_or_none()

    async def atualizar(self, prazo: Prazo, dados: dict) -> Prazo:
        for campo, valor in dados.items():
            setattr(prazo, campo, valor)
        await self.sessao.commit()
        await self.sessao.refresh(prazo)
        return prazo

    async def remover(self, prazo: Prazo) -> None:
        await self.sessao.delete(prazo)
        await self.sessao.commit()

    async def buscar_prova_mais_proxima(self, disciplina_id: int) -> Prazo | None:
        """Prova mais próxima (hoje em diante). Sem prova futura cadastrada -> None."""
        resultado = await self.sessao.execute(
            select(Prazo)
            .where(
                Prazo.disciplina_id == disciplina_id,
                Prazo.tipo == TipoPrazo.PROVA,
                Prazo.data >= date.today(),
            )
            .order_by(Prazo.data)
            .limit(1)
        )
        return resultado.scalar_one_or_none()

    async def listar_nao_concluidos_por_usuario(self, usuario_id: int) -> list[tuple[Prazo, str]]:
        resultado = await self.sessao.execute(
            select(Prazo, Disciplina.nome)
            .join(Disciplina, Prazo.disciplina_id == Disciplina.id)
            .where(Disciplina.usuario_id == usuario_id, Prazo.concluido.is_(False))
            .order_by(Prazo.data)
        )
        return [(linha.Prazo, linha.nome) for linha in resultado]
