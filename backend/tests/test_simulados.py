import json
import re

import pytest

from app.ia.fabrica import obter_provedor_texto
from app.main import app
from tests.conftest import cadastrar_e_logar, criar_disciplina, enviar_material_texto


class _ProvedorTextoSimuladoFixo:
    """Gera questões válidas, com quantidade extraída do próprio prompt."""

    async def gerar_texto(self, prompt: str) -> str:
        casamento = re.search(r"Crie exatamente (\d+)", prompt)
        quantidade = int(casamento.group(1)) if casamento else 1
        questoes = [
            {
                "enunciado": f"Pergunta {indice}?",
                "alternativas": ["A", "B", "C", "D"],
                "correta": 1,
                "explicacao": f"Explicação da questão {indice}.",
                "trecho_id": None,
            }
            for indice in range(quantidade)
        ]
        return json.dumps({"questoes": questoes})

    async def gerar_embedding(self, texto: str) -> list[float]:
        raise NotImplementedError


class _ProvedorTextoComFalhaTemporaria:
    """Responde com JSON inválido na primeira tentativa, depois com uma questão válida."""

    def __init__(self):
        self.tentativas = 0

    async def gerar_texto(self, prompt: str) -> str:
        self.tentativas += 1
        if self.tentativas == 1:
            return "isso não é um JSON válido"
        return json.dumps(
            {
                "questoes": [
                    {
                        "enunciado": "Pergunta?",
                        "alternativas": ["A", "B", "C", "D"],
                        "correta": 0,
                        "explicacao": "Explicação.",
                        "trecho_id": None,
                    }
                ]
            }
        )

    async def gerar_embedding(self, texto: str) -> list[float]:
        raise NotImplementedError


class _ProvedorTextoSempreInvalido:
    async def gerar_texto(self, prompt: str) -> str:
        return "ainda não é um JSON válido"

    async def gerar_embedding(self, texto: str) -> list[float]:
        raise NotImplementedError


class _ProvedorTextoComTrechoIdInvalido:
    async def gerar_texto(self, prompt: str) -> str:
        return json.dumps(
            {
                "questoes": [
                    {
                        "enunciado": "Pergunta?",
                        "alternativas": ["A", "B", "C", "D"],
                        "correta": 0,
                        "explicacao": "Explicação.",
                        "trecho_id": 999999999,
                    }
                ]
            }
        )

    async def gerar_embedding(self, texto: str) -> list[float]:
        raise NotImplementedError


async def _criar_material_com_trechos(cliente, cabecalhos, disciplina_id):
    criado = await enviar_material_texto(
        cliente, disciplina_id, cabecalhos, "Material", "Conteúdo de estudo sobre o assunto " * 20
    )
    return criado.json()["id"]


@pytest.mark.asyncio
async def test_gerar_simulado_retorna_quantidade_solicitada_sem_gabarito(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "sim1@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    material_id = await _criar_material_com_trechos(cliente, cabecalhos, disciplina_id)

    app.dependency_overrides[obter_provedor_texto] = lambda: _ProvedorTextoSimuladoFixo()

    resposta = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 3}, headers=cabecalhos
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert len(corpo["questoes"]) == 3
    for questao in corpo["questoes"]:
        assert "correta" not in questao
        assert "explicacao" not in questao
        assert len(questao["alternativas"]) == 4


@pytest.mark.asyncio
async def test_gerar_simulado_quantidade_invalida_retorna_422(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "sim2@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    material_id = await _criar_material_com_trechos(cliente, cabecalhos, disciplina_id)

    resposta = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 0}, headers=cabecalhos
    )

    assert resposta.status_code == 422


@pytest.mark.asyncio
async def test_material_sem_trechos_retorna_400_ao_gerar_simulado(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "sim3@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    criado = await enviar_material_texto(cliente, disciplina_id, cabecalhos, "Vazio", "   ")
    material_id = criado.json()["id"]

    resposta = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 1}, headers=cabecalhos
    )

    assert resposta.status_code == 400


@pytest.mark.asyncio
async def test_obter_simulado_nao_revela_gabarito(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "sim4@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    material_id = await _criar_material_com_trechos(cliente, cabecalhos, disciplina_id)

    app.dependency_overrides[obter_provedor_texto] = lambda: _ProvedorTextoSimuladoFixo()
    criado = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 2}, headers=cabecalhos
    )
    simulado_id = criado.json()["id"]

    resposta = await cliente.get(f"/simulados/{simulado_id}", headers=cabecalhos)

    assert resposta.status_code == 200
    for questao in resposta.json()["questoes"]:
        assert "correta" not in questao


@pytest.mark.asyncio
async def test_simulado_de_outro_usuario_retorna_404(cliente):
    cabecalhos_a = await cadastrar_e_logar(cliente, "sim5@exemplo.com")
    cabecalhos_b = await cadastrar_e_logar(cliente, "sim6@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos_a)
    material_id = await _criar_material_com_trechos(cliente, cabecalhos_a, disciplina_id)

    app.dependency_overrides[obter_provedor_texto] = lambda: _ProvedorTextoSimuladoFixo()
    criado = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 1}, headers=cabecalhos_a
    )
    simulado_id = criado.json()["id"]

    resposta = await cliente.get(f"/simulados/{simulado_id}", headers=cabecalhos_b)
    assert resposta.status_code == 404

    resposta_corrigir = await cliente.post(
        f"/simulados/{simulado_id}/corrigir", json={"respostas": []}, headers=cabecalhos_b
    )
    assert resposta_corrigir.status_code == 404


@pytest.mark.asyncio
async def test_corrigir_simulado_calcula_nota_e_monta_gabarito(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "sim7@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    material_id = await _criar_material_com_trechos(cliente, cabecalhos, disciplina_id)

    app.dependency_overrides[obter_provedor_texto] = lambda: _ProvedorTextoSimuladoFixo()
    criado = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 3}, headers=cabecalhos
    )
    simulado_id = criado.json()["id"]
    questoes = criado.json()["questoes"]

    respostas = [
        {"questao_id": questoes[0]["id"], "alternativa": 1},
        {"questao_id": questoes[1]["id"], "alternativa": 1},
        {"questao_id": questoes[2]["id"], "alternativa": 0},
    ]
    resposta = await cliente.post(
        f"/simulados/{simulado_id}/corrigir",
        json={"respostas": respostas},
        headers=cabecalhos,
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total"] == 3
    assert corpo["acertos"] == 2
    assert corpo["nota"] == pytest.approx(6.67, abs=0.01)
    item_errado = next(item for item in corpo["itens"] if item["questao_id"] == questoes[2]["id"])
    assert item_errado["acertou"] is False
    assert item_errado["correta"] == 1
    assert item_errado["escolhida"] == 0
    assert item_errado["explicacao"]


@pytest.mark.asyncio
async def test_llm_com_json_invalido_tenta_de_novo_e_consegue(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "sim8@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    material_id = await _criar_material_com_trechos(cliente, cabecalhos, disciplina_id)

    provedor = _ProvedorTextoComFalhaTemporaria()
    app.dependency_overrides[obter_provedor_texto] = lambda: provedor

    resposta = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 1}, headers=cabecalhos
    )

    assert resposta.status_code == 201
    assert provedor.tentativas == 2


@pytest.mark.asyncio
async def test_llm_sempre_invalido_retorna_502(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "sim9@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    material_id = await _criar_material_com_trechos(cliente, cabecalhos, disciplina_id)

    app.dependency_overrides[obter_provedor_texto] = lambda: _ProvedorTextoSempreInvalido()

    resposta = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 1}, headers=cabecalhos
    )

    assert resposta.status_code == 502


@pytest.mark.asyncio
async def test_trecho_id_fora_do_material_e_zerado(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "sim10@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    material_id = await _criar_material_com_trechos(cliente, cabecalhos, disciplina_id)

    app.dependency_overrides[obter_provedor_texto] = lambda: _ProvedorTextoComTrechoIdInvalido()
    criado = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 1}, headers=cabecalhos
    )
    simulado_id = criado.json()["id"]
    questao_id = criado.json()["questoes"][0]["id"]

    resposta = await cliente.post(
        f"/simulados/{simulado_id}/corrigir",
        json={"respostas": [{"questao_id": questao_id, "alternativa": 0}]},
        headers=cabecalhos,
    )

    assert resposta.json()["itens"][0]["trecho_id"] is None
