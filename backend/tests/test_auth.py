from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import jwt
import pytest
from sqlalchemy import delete

from app.config import configuracoes
from app.core.seguranca import ALGORITMO_JWT, verificar_senha
from app.models.usuario import Usuario
from tests.conftest import cadastrar_e_logar, fabrica_sessoes_teste


@pytest.mark.asyncio
async def test_cadastro_cria_usuario_com_sucesso(cliente):
    resposta = await cliente.post(
        "/auth/cadastro", json={"nome": "Ana", "email": "ana@exemplo.com", "senha": "senha1234"}
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["email"] == "ana@exemplo.com"
    assert "senha" not in corpo
    assert "senha_hash" not in corpo


@pytest.mark.asyncio
async def test_cadastro_com_email_duplicado_retorna_conflito(cliente):
    dados = {"nome": "Ana", "email": "ana2@exemplo.com", "senha": "senha1234"}
    await cliente.post("/auth/cadastro", json=dados)

    resposta = await cliente.post("/auth/cadastro", json=dados)

    assert resposta.status_code == 409
    assert resposta.json() == {"erro": "Email já cadastrado"}


@pytest.mark.asyncio
async def test_cadastro_com_senha_curta_retorna_erro_de_validacao(cliente):
    resposta = await cliente.post(
        "/auth/cadastro", json={"nome": "Ana", "email": "ana3@exemplo.com", "senha": "123"}
    )

    assert resposta.status_code == 422


@pytest.mark.asyncio
async def test_cadastro_com_email_invalido_retorna_422(cliente):
    resposta = await cliente.post(
        "/auth/cadastro", json={"nome": "Ana", "email": "nao-e-um-email", "senha": "senha1234"}
    )

    assert resposta.status_code == 422


@pytest.mark.asyncio
async def test_cadastro_com_nome_vazio_retorna_422(cliente):
    resposta = await cliente.post(
        "/auth/cadastro", json={"nome": "", "email": "ana4@exemplo.com", "senha": "senha1234"}
    )

    assert resposta.status_code == 422


@pytest.mark.asyncio
async def test_login_com_credenciais_corretas_retorna_token(cliente):
    dados = {"nome": "Bia", "email": "bia@exemplo.com", "senha": "senha1234"}
    await cliente.post("/auth/cadastro", json=dados)

    resposta = await cliente.post("/auth/login", json={"email": dados["email"], "senha": dados["senha"]})

    assert resposta.status_code == 200
    assert "access_token" in resposta.json()


@pytest.mark.asyncio
async def test_login_com_senha_errada_retorna_nao_autorizado(cliente):
    dados = {"nome": "Caio", "email": "caio@exemplo.com", "senha": "senha1234"}
    await cliente.post("/auth/cadastro", json=dados)

    resposta = await cliente.post(
        "/auth/login", json={"email": dados["email"], "senha": "senhaerrada"}
    )

    assert resposta.status_code == 401
    assert resposta.json() == {"erro": "Email ou senha inválidos"}


@pytest.mark.asyncio
async def test_eu_sem_token_retorna_nao_autorizado(cliente):
    resposta = await cliente.get("/auth/eu")

    assert resposta.status_code == 401


@pytest.mark.asyncio
async def test_eu_com_token_valido_retorna_usuario_logado(cliente):
    dados = {"nome": "Duda", "email": "duda@exemplo.com", "senha": "senha1234"}
    await cliente.post("/auth/cadastro", json=dados)
    login = await cliente.post(
        "/auth/login", json={"email": dados["email"], "senha": dados["senha"]}
    )
    token = login.json()["access_token"]

    resposta = await cliente.get("/auth/eu", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 200
    assert resposta.json()["email"] == dados["email"]


@pytest.mark.asyncio
async def test_eu_com_token_expirado_retorna_401(cliente):
    dados = {"nome": "Eva", "email": "eva@exemplo.com", "senha": "senha1234"}
    cadastro = await cliente.post("/auth/cadastro", json=dados)
    usuario_id = cadastro.json()["id"]

    token_expirado = jwt.encode(
        {"sub": str(usuario_id), "exp": datetime.now(UTC) - timedelta(minutes=1)},
        configuracoes.JWT_SECRET,
        algorithm=ALGORITMO_JWT,
    )

    resposta = await cliente.get("/auth/eu", headers={"Authorization": f"Bearer {token_expirado}"})

    assert resposta.status_code == 401


@pytest.mark.asyncio
async def test_eu_com_token_malformado_retorna_401(cliente):
    resposta = await cliente.get("/auth/eu", headers={"Authorization": "Bearer isso.nao.e.um.jwt"})

    assert resposta.status_code == 401


@pytest.mark.asyncio
async def test_eu_sem_prefixo_bearer_retorna_401(cliente):
    dados = {"nome": "Fe", "email": "fe@exemplo.com", "senha": "senha1234"}
    await cliente.post("/auth/cadastro", json=dados)
    login = await cliente.post("/auth/login", json={"email": dados["email"], "senha": dados["senha"]})
    token = login.json()["access_token"]

    resposta = await cliente.get("/auth/eu", headers={"Authorization": token})

    assert resposta.status_code == 401


@pytest.mark.asyncio
async def test_token_de_usuario_deletado_retorna_401(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "del@exemplo.com")

    async with fabrica_sessoes_teste() as sessao:
        await sessao.execute(delete(Usuario).where(Usuario.email == "del@exemplo.com"))
        await sessao.commit()

    resposta = await cliente.get("/auth/eu", headers=cabecalhos)

    assert resposta.status_code == 401


@pytest.mark.asyncio
async def test_login_com_email_inexistente_tambem_verifica_um_hash(cliente):
    """Evita o canal lateral de tempo: mesmo sem usuário, o verificar_senha precisa rodar."""
    with patch("app.services.autenticacao_servico.verificar_senha", wraps=verificar_senha) as espiao:
        resposta = await cliente.post(
            "/auth/login", json={"email": "nao-existe@exemplo.com", "senha": "qualquercoisa123"}
        )

    assert resposta.status_code == 401
    assert espiao.called
