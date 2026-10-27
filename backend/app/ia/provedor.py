from typing import Protocol


class ProvedorIA(Protocol):
    """Interface comum para geração de texto e de embeddings."""

    async def gerar_texto(self, prompt: str) -> str: ...

    async def gerar_embedding(self, texto: str) -> list[float]: ...
