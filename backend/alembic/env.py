import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.config import configuracoes

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


def run_migrations_offline() -> None:
    """Gera SQL sem conectar ao banco."""
    context.configure(
        url=configuracoes.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def executar_migracoes_sincronas(conexao) -> None:
    context.configure(connection=conexao, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Conecta ao banco de forma assíncrona e aplica as migrações."""
    motor = create_async_engine(configuracoes.DATABASE_URL)

    async with motor.connect() as conexao:
        await conexao.run_sync(executar_migracoes_sincronas)

    await motor.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
