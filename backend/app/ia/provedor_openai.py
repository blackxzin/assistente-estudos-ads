import httpx


class ProvedorOpenAI:
    """Chama a API da OpenAI para texto e embeddings."""

    def __init__(
        self,
        chave_api: str,
        modelo_texto: str = "gpt-4o-mini",
        modelo_embedding: str = "text-embedding-3-small",
    ):
        self.chave_api = chave_api
        self.modelo_texto = modelo_texto
        self.modelo_embedding = modelo_embedding

    async def gerar_texto(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30) as cliente:
            resposta = await cliente.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.chave_api}"},
                json={"model": self.modelo_texto, "messages": [{"role": "user", "content": prompt}]},
            )
            resposta.raise_for_status()
            return resposta.json()["choices"][0]["message"]["content"]

    async def gerar_embedding(self, texto: str) -> list[float]:
        async with httpx.AsyncClient(timeout=30) as cliente:
            resposta = await cliente.post(
                "https://api.openai.com/v1/embeddings",
                headers={"Authorization": f"Bearer {self.chave_api}"},
                json={"model": self.modelo_embedding, "input": texto},
            )
            resposta.raise_for_status()
            return resposta.json()["data"][0]["embedding"]
