from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import configuracoes

motor = create_async_engine(configuracoes.DATABASE_URL, pool_pre_ping=True)

fabrica_sessoes = async_sessionmaker(motor, expire_on_commit=False)


async def obter_sessao() -> AsyncGenerator[AsyncSession, None]:
    """Cria uma sessão de banco por requisição e garante o fechamento."""
    async with fabrica_sessoes() as sessao:
        yield sessao
