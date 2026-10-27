from app.config import configuracoes
from app.core.erros import NaoEncontrado
from app.ia.provedor import ProvedorIA
from app.repositories.material_repositorio import MaterialRepositorio
from app.repositories.trecho_repositorio import TrechoRepositorio
from app.schemas.pergunta import CitacaoResposta, RespostaPergunta

MENSAGEM_SEM_RESPOSTA = "Não encontrei isso no material."


def _montar_prompt(pergunta: str, trechos: list[tuple]) -> str:
    contexto = "\n\n".join(
        f"[Trecho {i + 1}] {trecho.conteudo}" for i, (trecho, _distancia) in enumerate(trechos)
    )
    return (
        "Responda a pergunta do usuário usando exclusivamente os trechos abaixo. "
        "Se a resposta não estiver neles, diga que não sabe.\n\n"
        f"Trechos:\n{contexto}\n\nPergunta: {pergunta}"
    )


class QAServico:
    def __init__(
        self,
        repositorio_trecho: TrechoRepositorio,
        repositorio_material: MaterialRepositorio,
        provedor_embedding: ProvedorIA,
        provedor_texto: ProvedorIA,
    ):
        self.repositorio_trecho = repositorio_trecho
        self.repositorio_material = repositorio_material
        self.provedor_embedding = provedor_embedding
        self.provedor_texto = provedor_texto

    async def perguntar(self, material_id: int, usuario_id: int, pergunta: str) -> RespostaPergunta:
        material = await self.repositorio_material.buscar_por_id_e_usuario(material_id, usuario_id)
        if material is None:
            raise NaoEncontrado("Material não encontrado")

        vetor_pergunta = await self.provedor_embedding.gerar_embedding(pergunta)
        resultados = await self.repositorio_trecho.buscar_mais_similares(
            material_id, vetor_pergunta, configuracoes.TOP_K_BUSCA
        )

        melhor_similaridade = 1 - resultados[0][1] if resultados else 0.0
        if melhor_similaridade < configuracoes.LIMIAR_SIMILARIDADE:
            return RespostaPergunta(resposta=MENSAGEM_SEM_RESPOSTA, citacoes=[])

        resposta_texto = await self.provedor_texto.gerar_texto(_montar_prompt(pergunta, resultados))
        citacoes = [
            CitacaoResposta(trecho_id=trecho.id, pagina=trecho.pagina, trecho=trecho.conteudo)
            for trecho, _distancia in resultados
        ]
        return RespostaPergunta(resposta=resposta_texto, citacoes=citacoes)
