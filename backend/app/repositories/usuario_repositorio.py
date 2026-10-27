from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import Usuario


class UsuarioRepositorio:
    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao

    async def buscar_por_email(self, email: str) -> Usuario | None:
        resultado = await self.sessao.execute(select(Usuario).where(Usuario.email == email))
        return resultado.scalar_one_or_none()

    async def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        resultado = await self.sessao.execute(select(Usuario).where(Usuario.id == usuario_id))
        return resultado.scalar_one_or_none()

    async def criar(self, nome: str, email: str, senha_hash: str) -> Usuario:
        usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
        self.sessao.add(usuario)
        await self.sessao.commit()
        await self.sessao.refresh(usuario)
        return usuario
