import pytest

from app.config import configuracoes


@pytest.mark.asyncio
async def test_login_bloqueia_apos_exceder_limite_de_tentativas(cliente, monkeypatch):
    monkeypatch.setattr(configuracoes, "RATE_LIMIT_MAX_REQUISICOES", 3)

    for _ in range(3):
        await cliente.post("/auth/login", json={"email": "alguem@exemplo.com", "senha": "errada123"})

    resposta = await cliente.post(
        "/auth/login", json={"email": "alguem@exemplo.com", "senha": "errada123"}
    )

    assert resposta.status_code == 429
    assert "erro" in resposta.json()


@pytest.mark.asyncio
async def test_cadastro_tambem_e_limitado_por_ip(cliente, monkeypatch):
    monkeypatch.setattr(configuracoes, "RATE_LIMIT_MAX_REQUISICOES", 2)

    for indice in range(2):
        await cliente.post(
            "/auth/cadastro",
            json={"nome": "N", "email": f"rl{indice}@exemplo.com", "senha": "senha1234"},
        )

    resposta = await cliente.post(
        "/auth/cadastro", json={"nome": "N", "email": "rl99@exemplo.com", "senha": "senha1234"}
    )

    assert resposta.status_code == 429


@pytest.mark.asyncio
async def test_limite_expira_apos_a_janela(cliente, monkeypatch):
    monkeypatch.setattr(configuracoes, "RATE_LIMIT_MAX_REQUISICOES", 1)
    monkeypatch.setattr(configuracoes, "RATE_LIMIT_JANELA_SEGUNDOS", 0)

    primeira = await cliente.post(
        "/auth/login", json={"email": "janela@exemplo.com", "senha": "errada123"}
    )
    segunda = await cliente.post(
        "/auth/login", json={"email": "janela@exemplo.com", "senha": "errada123"}
    )

    assert primeira.status_code != 429
    assert segunda.status_code != 429
