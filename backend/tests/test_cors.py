import pytest

from app.config import configuracoes


@pytest.mark.asyncio
async def test_preflight_libera_origem_configurada(cliente):
    resposta = await cliente.options(
        "/disciplinas",
        headers={
            "Origin": configuracoes.origens_cors[0],
            "Access-Control-Request-Method": "GET",
        },
    )

    assert resposta.status_code == 200
    assert resposta.headers["access-control-allow-origin"] == configuracoes.origens_cors[0]


@pytest.mark.asyncio
async def test_preflight_de_origem_nao_configurada_nao_libera(cliente):
    resposta = await cliente.options(
        "/disciplinas",
        headers={
            "Origin": "http://origem-nao-permitida.com",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" not in resposta.headers
