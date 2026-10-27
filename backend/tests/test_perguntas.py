import pytest

from app.config import configuracoes
from app.ia.fabrica import obter_provedor_embedding, obter_provedor_texto
from app.main import app
from tests.conftest import cadastrar_e_logar, criar_disciplina, enviar_material_texto


def _vetor_unitario(indice: int) -> list[float]:
    vetor = [0.0] * configuracoes.EMBEDDING_DIM
    vetor[indice % configuracoes.EMBEDDING_DIM] = 1.0
    return vetor


class _ProvedorEmbeddingDeterministico:
    """Gera vetores previsíveis: mesma categoria de texto -> mesmo vetor, para controlar a similaridade."""

    async def gerar_embedding(self, texto: str) -> list[float]:
        texto_normalizado = texto.lower()
        if "gato" in texto_normalizado:
            return _vetor_unitario(0)
        if "carro" in texto_normalizado:
            return _vetor_unitario(1)
        return _vetor_unitario(2)

    async def gerar_texto(self, prompt: str) -> str:
        return "não deveria ser chamado neste provedor"


class _ProvedorTextoEspiao:
    def __init__(self):
        self.chamadas = 0

    async def gerar_texto(self, prompt: str) -> str:
        self.chamadas += 1
        return "Resposta gerada a partir dos trechos fornecidos."

    async def gerar_embedding(self, texto: str) -> list[float]:
        raise NotImplementedError


@pytest.mark.asyncio
async def test_pergunta_relacionada_ao_material_retorna_resposta_com_citacao(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "pergunta1@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)

    espiao = _ProvedorTextoEspiao()
    app.dependency_overrides[obter_provedor_embedding] = lambda: _ProvedorEmbeddingDeterministico()
    app.dependency_overrides[obter_provedor_texto] = lambda: espiao

    criado = await enviar_material_texto(
        cliente, disciplina_id, cabecalhos, "Sobre gatos", "Gatos são mamíferos e gostam de dormir bastante."
    )
    material_id = criado.json()["id"]

    resposta = await cliente.post(
        f"/materiais/{material_id}/perguntas",
        json={"pergunta": "O que você sabe sobre gatos?"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["resposta"] == "Resposta gerada a partir dos trechos fornecidos."
    assert len(corpo["citacoes"]) == 1
    assert espiao.chamadas == 1


@pytest.mark.asyncio
async def test_pergunta_nao_relacionada_nao_chama_llm_e_avisa_que_nao_encontrou(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "pergunta2@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)

    espiao = _ProvedorTextoEspiao()
    app.dependency_overrides[obter_provedor_embedding] = lambda: _ProvedorEmbeddingDeterministico()
    app.dependency_overrides[obter_provedor_texto] = lambda: espiao

    criado = await enviar_material_texto(
        cliente, disciplina_id, cabecalhos, "Sobre gatos", "Gatos são mamíferos e gostam de dormir bastante."
    )
    material_id = criado.json()["id"]

    resposta = await cliente.post(
        f"/materiais/{material_id}/perguntas",
        json={"pergunta": "Qual o motor de um carro?"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["resposta"] == "Não encontrei isso no material."
    assert corpo["citacoes"] == []
    assert espiao.chamadas == 0
