import pytest

from app.config import configuracoes
from app.ia.fabrica import obter_provedor_embedding, obter_provedor_texto
from app.ia.provedor_falso import ProvedorFalso
from app.main import app
from tests.conftest import cadastrar_e_logar, criar_disciplina, enviar_material_texto


class _ProvedorTextoComResumoFixo:
    async def gerar_texto(self, prompt: str) -> str:
        return "- Ponto 1\n- Ponto 2"

    async def gerar_embedding(self, texto: str) -> list[float]:
        raise NotImplementedError


@pytest.mark.asyncio
async def test_gerar_resumo_salva_e_retorna_resumo_do_material(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "resumo1@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)

    app.dependency_overrides[obter_provedor_embedding] = lambda: ProvedorFalso(configuracoes.EMBEDDING_DIM)
    app.dependency_overrides[obter_provedor_texto] = lambda: _ProvedorTextoComResumoFixo()

    criado = await enviar_material_texto(
        cliente,
        disciplina_id,
        cabecalhos,
        "Material para resumir",
        "Texto longo sobre o assunto da disciplina.",
    )
    material_id = criado.json()["id"]

    resposta = await cliente.post(f"/materiais/{material_id}/resumo", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json()["resumo"] == "- Ponto 1\n- Ponto 2"

    buscado = await cliente.get(f"/materiais/{material_id}", headers=cabecalhos)
    assert buscado.json()["resumo"] == "- Ponto 1\n- Ponto 2"
