import pytest

from app.config import configuracoes
from tests.conftest import cadastrar_e_logar, criar_disciplina, enviar_material_texto


@pytest.mark.asyncio
async def test_estourar_limite_diario_de_ia_retorna_429(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "limite1@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    criado = await enviar_material_texto(cliente, disciplina_id, cabecalhos, "Material", "Texto de teste")
    material_id = criado.json()["id"]

    ultima_resposta = None
    for _ in range(configuracoes.LIMITE_IA_DIARIO + 1):
        ultima_resposta = await cliente.post(f"/materiais/{material_id}/resumo", headers=cabecalhos)

    assert ultima_resposta.status_code == 429
    assert "erro" in ultima_resposta.json()


@pytest.mark.asyncio
async def test_limite_diario_e_compartilhado_entre_endpoints_de_ia(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "limite2@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    criado = await enviar_material_texto(cliente, disciplina_id, cabecalhos, "Material", "Texto de teste")
    material_id = criado.json()["id"]

    for _ in range(configuracoes.LIMITE_IA_DIARIO):
        await cliente.post(
            f"/materiais/{material_id}/perguntas", json={"pergunta": "oi"}, headers=cabecalhos
        )

    resposta = await cliente.post(f"/materiais/{material_id}/resumo", headers=cabecalhos)

    assert resposta.status_code == 429


@pytest.mark.asyncio
async def test_limite_diario_e_isolado_por_usuario(cliente):
    cabecalhos_a = await cadastrar_e_logar(cliente, "limite3@exemplo.com")
    cabecalhos_b = await cadastrar_e_logar(cliente, "limite4@exemplo.com")
    disciplina_a = await criar_disciplina(cliente, cabecalhos_a)
    disciplina_b = await criar_disciplina(cliente, cabecalhos_b)
    material_a = (await enviar_material_texto(cliente, disciplina_a, cabecalhos_a, "M", "Texto")).json()["id"]
    material_b = (await enviar_material_texto(cliente, disciplina_b, cabecalhos_b, "M", "Texto")).json()["id"]

    for _ in range(configuracoes.LIMITE_IA_DIARIO + 1):
        await cliente.post(f"/materiais/{material_a}/resumo", headers=cabecalhos_a)

    resposta_b = await cliente.post(f"/materiais/{material_b}/resumo", headers=cabecalhos_b)

    assert resposta_b.status_code == 200
