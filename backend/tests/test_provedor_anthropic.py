from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.ia.provedor_anthropic import ProvedorAnthropic


@pytest.mark.asyncio
async def test_gerar_texto_retorna_conteudo_da_resposta():
    resposta_falsa = httpx.Response(
        200,
        json={"content": [{"text": "resposta da claude"}]},
        request=httpx.Request("POST", "https://exemplo.com"),
    )

    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=resposta_falsa)):
        provedor = ProvedorAnthropic("chave-falsa")
        resultado = await provedor.gerar_texto("prompt qualquer")

    assert resultado == "resposta da claude"


@pytest.mark.asyncio
async def test_gerar_embedding_nao_e_suportado():
    provedor = ProvedorAnthropic("chave-falsa")

    with pytest.raises(NotImplementedError):
        await provedor.gerar_embedding("texto")
