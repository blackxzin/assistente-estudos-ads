import pytest


@pytest.mark.asyncio
async def test_saude_retorna_ok_quando_banco_responde(cliente):
    resposta = await cliente.get("/saude")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok", "banco": "conectado"}
