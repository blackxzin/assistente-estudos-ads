from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trecho import Trecho


class TrechoRepositorio:
    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao

    async def criar(
        self, material_id: int, conteudo: str, pagina: int | None, posicao: int, embedding: list[float]
    ) -> Trecho:
        trecho = Trecho(
            material_id=material_id, conteudo=conteudo, pagina=pagina, posicao=posicao, embedding=embedding
        )
        self.sessao.add(trecho)
        await self.sessao.commit()
        await self.sessao.refresh(trecho)
        return trecho

    async def listar_por_material(self, material_id: int) -> list[Trecho]:
        resultado = await self.sessao.execute(
            select(Trecho).where(Trecho.material_id == material_id).order_by(Trecho.posicao)
        )
        return list(resultado.scalars().all())

    async def buscar_mais_similares(
        self, material_id: int, vetor_pergunta: list[float], top_k: int
    ) -> list[tuple[Trecho, float]]:
        """Retorna pares (trecho, distância_cosseno) ordenados do mais ao menos similar."""
        distancia = Trecho.embedding.cosine_distance(vetor_pergunta)
        resultado = await self.sessao.execute(
            select(Trecho, distancia.label("distancia"))
            .where(Trecho.material_id == material_id)
            .order_by(distancia)
            .limit(top_k)
        )
        return [(linha.Trecho, linha.distancia) for linha in resultado]
