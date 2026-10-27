from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.disciplina import Disciplina


class DisciplinaRepositorio:
    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao

    async def criar(self, usuario_id: int, nome: str, professor: str | None, cor: str | None) -> Disciplina:
        disciplina = Disciplina(usuario_id=usuario_id, nome=nome, professor=professor, cor=cor)
        self.sessao.add(disciplina)
        await self.sessao.commit()
        await self.sessao.refresh(disciplina)
        return disciplina

    async def listar_por_usuario(self, usuario_id: int) -> list[Disciplina]:
        resultado = await self.sessao.execute(select(Disciplina).where(Disciplina.usuario_id == usuario_id))
        return list(resultado.scalars().all())

    async def buscar_por_id_e_usuario(self, disciplina_id: int, usuario_id: int) -> Disciplina | None:
        resultado = await self.sessao.execute(
            select(Disciplina).where(Disciplina.id == disciplina_id, Disciplina.usuario_id == usuario_id)
        )
        return resultado.scalar_one_or_none()

    async def atualizar(self, disciplina: Disciplina, dados: dict) -> Disciplina:
        for campo, valor in dados.items():
            setattr(disciplina, campo, valor)
        await self.sessao.commit()
        await self.sessao.refresh(disciplina)
        return disciplina

    async def remover(self, disciplina: Disciplina) -> None:
        await self.sessao.delete(disciplina)
        await self.sessao.commit()
