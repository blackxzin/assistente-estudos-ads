import json
from datetime import date, timedelta

import pytest
from sqlalchemy import update

from app.ia.fabrica import obter_provedor_texto
from app.main import app
from app.models.revisao import Revisao
from tests.conftest import cadastrar_e_logar, criar_disciplina, enviar_material_texto, fabrica_sessoes_teste

HOJE = date.today()


class _ProvedorTextoSimuladoFixo:
    async def gerar_texto(self, prompt: str) -> str:
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


@pytest.mark.asyncio
async def test_painel_agrega_prazos_revisoes_e_desempenho(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "painel1@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)

    pendente = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={
            "titulo": "Trabalho pendente",
            "tipo": "trabalho",
            "data": (HOJE + timedelta(days=2)).isoformat(),
        },
        headers=cabecalhos,
    )
    prazo_pendente_id = pendente.json()["id"]

    concluido = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={"titulo": "Trabalho concluído", "tipo": "trabalho", "data": HOJE.isoformat()},
        headers=cabecalhos,
    )
    await cliente.put(f"/prazos/{concluido.json()['id']}", json={"concluido": True}, headers=cabecalhos)

    criado = await enviar_material_texto(cliente, disciplina_id, cabecalhos, "Material", "Conteúdo")
    material_id = criado.json()["id"]

    async with fabrica_sessoes_teste() as sessao:
        await sessao.execute(update(Revisao).values(data_prevista=HOJE))
        await sessao.commit()

    app.dependency_overrides[obter_provedor_texto] = lambda: _ProvedorTextoSimuladoFixo()
    simulado = await cliente.post(
        f"/materiais/{material_id}/simulados", json={"quantidade": 1}, headers=cabecalhos
    )
    questao_id = simulado.json()["questoes"][0]["id"]
    await cliente.post(
        f"/simulados/{simulado.json()['id']}/corrigir",
        json={"respostas": [{"questao_id": questao_id, "alternativa": 0}]},
        headers=cabecalhos,
    )

    resposta = await cliente.get("/painel", headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()

    ids_prazos = [p["id"] for p in corpo["proximos_prazos"]]
    assert prazo_pendente_id in ids_prazos
    assert concluido.json()["id"] not in ids_prazos

    assert len(corpo["revisoes_hoje"]) == 1
    assert corpo["revisoes_hoje"][0]["material_id"] == material_id

    assert corpo["desempenho"]["total_simulados"] == 1
    assert corpo["desempenho"]["media_nota"] == pytest.approx(10.0)
    assert corpo["desempenho"]["ultimos"][0]["nota"] == pytest.approx(10.0)


@pytest.mark.asyncio
async def test_painel_sem_dados_retorna_listas_vazias_e_media_nula(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "painel2@exemplo.com")

    resposta = await cliente.get("/painel", headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["proximos_prazos"] == []
    assert corpo["revisoes_hoje"] == []
    assert corpo["desempenho"]["media_nota"] is None
    assert corpo["desempenho"]["total_simulados"] == 0
    assert corpo["desempenho"]["ultimos"] == []
