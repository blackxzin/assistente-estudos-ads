import os
import subprocess
import sys
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core import limite_taxa
from app.database import obter_sessao
from app.main import app
from app.models import Base

URL_BANCO_TESTE = os.environ.get("TEST_DATABASE_URL") or os.environ["DATABASE_URL"]
DIRETORIO_BACKEND = Path(__file__).resolve().parent.parent

motor_teste = create_async_engine(URL_BANCO_TESTE)
fabrica_sessoes_teste = async_sessionmaker(motor_teste, expire_on_commit=False)


def _rodar_alembic(*args: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "alembic", *args], cwd=DIRETORIO_BACKEND, check=True, env=os.environ
    )


@pytest.fixture(scope="session", autouse=True)
async def preparar_banco():
    """Recria o esquema do banco de teste via alembic (não Base.metadata), uma vez por sessão.

    Rodar as migrações de verdade (em vez de Base.metadata.create_all) garante que os testes
    quebrem se o modelo SQLAlchemy divergir do que a migração realmente cria no banco.
    """
    async with motor_teste.begin() as conexao:
        await conexao.execute(text("DROP SCHEMA public CASCADE"))
        await conexao.execute(text("CREATE SCHEMA public"))

    _rodar_alembic("upgrade", "head")

    yield
    await motor_teste.dispose()


@pytest.fixture(autouse=True)
async def limpar_tabelas(preparar_banco):
    """Esvazia as tabelas antes de cada teste, para isolar os casos."""
    async with motor_teste.begin() as conexao:
        for tabela in reversed(Base.metadata.sorted_tables):
            await conexao.execute(tabela.delete())
    yield


@pytest.fixture(autouse=True)
def _limpar_limitador_de_taxa():
    """Zera o limitador de taxa de /auth antes de cada teste, para não acumular entre casos."""
    limite_taxa.limpar_registros()
    yield


async def _sessao_teste() -> AsyncGenerator:
    async with fabrica_sessoes_teste() as sessao:
        yield sessao


@pytest.fixture
async def cliente() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[obter_sessao] = _sessao_teste
    transporte = ASGITransport(app=app)
    async with AsyncClient(transport=transporte, base_url="http://test") as cliente_http:
        yield cliente_http
    app.dependency_overrides.clear()


async def cadastrar_e_logar(cliente: AsyncClient, email: str) -> dict:
    dados = {"nome": "Usuario Teste", "email": email, "senha": "senha1234"}
    await cliente.post("/auth/cadastro", json=dados)
    login = await cliente.post("/auth/login", json={"email": email, "senha": dados["senha"]})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def criar_disciplina(cliente: AsyncClient, cabecalhos: dict, nome: str = "Disciplina Teste") -> int:
    resposta = await cliente.post("/disciplinas", json={"nome": nome}, headers=cabecalhos)
    return resposta.json()["id"]


async def enviar_material_texto(
    cliente: AsyncClient, disciplina_id: int, cabecalhos: dict, titulo: str, texto: str
):
    return await cliente.post(
        f"/disciplinas/{disciplina_id}/materiais",
        data={"titulo": titulo},
        files={"arquivo_texto": ("material.txt", texto.encode("utf-8"), "text/plain")},
        headers=cabecalhos,
    )
