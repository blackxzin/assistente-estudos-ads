from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.ia.provedor_openai import ProvedorOpenAI


def _resposta(json_body: dict) -> httpx.Response:
    return httpx.Response(200, json=json_body, request=httpx.Request("POST", "https://exemplo.com"))


@pytest.mark.asyncio
async def test_gerar_texto_retorna_conteudo_da_resposta():
    resposta_falsa = _resposta({"choices": [{"message": {"content": "resposta do modelo"}}]})

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=resposta_falsa)):
        provedor = ProvedorOpenAI("chave-falsa")
        resultado = await provedor.gerar_texto("prompt qualquer")

    assert resultado == "resposta do modelo"


@pytest.mark.asyncio
async def test_gerar_embedding_retorna_vetor_da_resposta():
    resposta_falsa = _resposta({"data": [{"embedding": [0.1, 0.2, 0.3]}]})

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=resposta_falsa)):
        provedor = ProvedorOpenAI("chave-falsa")
        resultado = await provedor.gerar_embedding("texto qualquer")

    assert resultado == [0.1, 0.2, 0.3]


@pytest.mark.asyncio
async def test_gerar_texto_propaga_erro_http():
    resposta_falsa = httpx.Response(
        401, json={"error": "unauthorized"}, request=httpx.Request("POST", "https://exemplo.com")
    )

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=resposta_falsa)):
        provedor = ProvedorOpenAI("chave-invalida")
        with pytest.raises(httpx.HTTPStatusError):
            await provedor.gerar_texto("prompt")
