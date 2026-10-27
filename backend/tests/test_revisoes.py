from datetime import date, timedelta

import pytest
from sqlalchemy import select, update

from app.models.revisao import Revisao, StatusRevisao
from tests.conftest import cadastrar_e_logar, criar_disciplina, enviar_material_texto, fabrica_sessoes_teste

HOJE = date.today()


async def _criar_material_pronto(cliente, cabecalhos, disciplina_id, titulo="Material"):
    criado = await enviar_material_texto(cliente, disciplina_id, cabecalhos, titulo, "Conteúdo de estudo")
    return criado.json()["id"]


@pytest.mark.asyncio
async def test_material_pronto_agenda_revisao_inicial_em_um_dia(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "rev1@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    await _criar_material_pronto(cliente, cabecalhos, disciplina_id)

    resposta = await cliente.get(
        f"/revisoes?de={HOJE.isoformat()}&ate={(HOJE + timedelta(days=5)).isoformat()}",
        headers=cabecalhos,
    )

    assert resposta.status_code == 200
    revisoes = resposta.json()
    assert len(revisoes) == 1
    assert revisoes[0]["etapa"] == 0
    assert revisoes[0]["status"] == "pendente"
    assert revisoes[0]["data_prevista"] == (HOJE + timedelta(days=1)).isoformat()
    assert revisoes[0]["material_titulo"] == "Material"
    assert revisoes[0]["disciplina_nome"]


@pytest.mark.asyncio
async def test_listar_revisoes_com_periodo_invertido_retorna_400(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "rev2@exemplo.com")

    resposta = await cliente.get(
        f"/revisoes?de={HOJE.isoformat()}&ate={(HOJE - timedelta(days=1)).isoformat()}",
        headers=cabecalhos,
    )

    assert resposta.status_code == 400


@pytest.mark.asyncio
async def test_concluir_revisao_com_lembrei_avanca_etapa_e_agenda_proxima(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "rev3@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    await _criar_material_pronto(cliente, cabecalhos, disciplina_id)

    listagem = await cliente.get(
        f"/revisoes?de={HOJE.isoformat()}&ate={(HOJE + timedelta(days=5)).isoformat()}",
        headers=cabecalhos,
    )
    revisao_id = listagem.json()[0]["id"]

    resposta = await cliente.post(
        f"/revisoes/{revisao_id}/concluir", json={"desempenho": "lembrei"}, headers=cabecalhos
    )

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "feita"

    listagem_futura = await cliente.get(
        f"/revisoes?de={HOJE.isoformat()}&ate={(HOJE + timedelta(days=10)).isoformat()}",
        headers=cabecalhos,
    )
    revisoes = listagem_futura.json()
    pendentes = [r for r in revisoes if r["status"] == "pendente"]
    assert len(pendentes) == 1
    assert pendentes[0]["etapa"] == 1
    assert pendentes[0]["data_prevista"] == (HOJE + timedelta(days=3)).isoformat()


@pytest.mark.asyncio
async def test_concluir_revisao_de_outro_usuario_retorna_404(cliente):
    cabecalhos_a = await cadastrar_e_logar(cliente, "rev4@exemplo.com")
    cabecalhos_b = await cadastrar_e_logar(cliente, "rev5@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos_a)
    await _criar_material_pronto(cliente, cabecalhos_a, disciplina_id)

    listagem = await cliente.get(
        f"/revisoes?de={HOJE.isoformat()}&ate={(HOJE + timedelta(days=5)).isoformat()}",
        headers=cabecalhos_a,
    )
    revisao_id = listagem.json()[0]["id"]

    resposta = await cliente.post(
        f"/revisoes/{revisao_id}/concluir", json={"desempenho": "lembrei"}, headers=cabecalhos_b
    )

    assert resposta.status_code == 404


@pytest.mark.asyncio
async def test_criar_prova_reagenda_revisoes_pendentes_que_ultrapassariam_a_data(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "rev6@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    await _criar_material_pronto(cliente, cabecalhos, disciplina_id)

    data_distante = HOJE + timedelta(days=30)
    async with fabrica_sessoes_teste() as sessao:
        await sessao.execute(update(Revisao).values(data_prevista=data_distante, etapa=4))
        await sessao.commit()

    data_prova = HOJE + timedelta(days=5)
    resposta_prazo = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={"titulo": "Prova final", "tipo": "prova", "data": data_prova.isoformat()},
        headers=cabecalhos,
    )
    assert resposta_prazo.status_code == 201

    async with fabrica_sessoes_teste() as sessao:
        resultado = await sessao.execute(select(Revisao))
        revisao = resultado.scalar_one()

    assert revisao.data_prevista < data_prova
    assert revisao.data_prevista > HOJE
    assert revisao.status == StatusRevisao.PENDENTE


@pytest.mark.asyncio
async def test_alterar_prazo_para_prova_tambem_reagenda_revisoes(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "rev7@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    await _criar_material_pronto(cliente, cabecalhos, disciplina_id)

    data_distante = HOJE + timedelta(days=30)
    async with fabrica_sessoes_teste() as sessao:
        await sessao.execute(update(Revisao).values(data_prevista=data_distante, etapa=4))
        await sessao.commit()

    criado = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={"titulo": "Trabalho", "tipo": "trabalho", "data": (HOJE + timedelta(days=5)).isoformat()},
        headers=cabecalhos,
    )
    prazo_id = criado.json()["id"]

    data_prova = HOJE + timedelta(days=4)
    resposta = await cliente.put(
        f"/prazos/{prazo_id}",
        json={"tipo": "prova", "data": data_prova.isoformat()},
        headers=cabecalhos,
    )
    assert resposta.status_code == 200

    async with fabrica_sessoes_teste() as sessao:
        resultado = await sessao.execute(select(Revisao))
        revisao = resultado.scalar_one()

    assert revisao.data_prevista < data_prova
