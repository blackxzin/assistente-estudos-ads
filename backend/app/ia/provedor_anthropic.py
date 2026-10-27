import httpx


class ProvedorAnthropic:
    """Chama a API da Anthropic para texto. Não oferece embeddings."""

    def __init__(self, chave_api: str, modelo: str = "claude-3-5-haiku-20241022"):
        self.chave_api = chave_api
        self.modelo = modelo

    async def gerar_texto(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30) as cliente:
            resposta = await cliente.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": self.chave_api, "anthropic-version": "2023-06-01"},
                json={
                    "model": self.modelo,
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            resposta.raise_for_status()
            return resposta.json()["content"][0]["text"]

    async def gerar_embedding(self, texto: str) -> list[float]:
        raise NotImplementedError(
            "Anthropic não oferece embeddings; configure EMBEDDING_PROVEDOR=openai"
        )
