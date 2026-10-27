import pytest

from app.models.material import StatusMaterial, TipoMaterial
from tests.ajuda_pdf import gerar_pdf_bytes
from tests.conftest import cadastrar_e_logar, criar_disciplina, enviar_material_texto


@pytest.mark.asyncio
async def test_upload_de_texto_cria_material_pronto_com_trechos(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "mat1@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)

    resposta = await enviar_material_texto(
        cliente, disciplina_id, cabecalhos, "Notas de aula", "Conteudo de estudo " * 50
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["status"] == StatusMaterial.PRONTO.value
    assert corpo["tipo"] == TipoMaterial.TEXTO.value


@pytest.mark.asyncio
async def test_upload_de_pdf_real_cria_material_pronto(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "mat2@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    pdf_bytes = gerar_pdf_bytes(["Conteudo do PDF de teste"])

    resposta = await cliente.post(
        f"/disciplinas/{disciplina_id}/materiais",
        data={"titulo": "Slides"},
        files={"arquivo": ("slides.pdf", pdf_bytes, "application/pdf")},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    assert resposta.json()["status"] == StatusMaterial.PRONTO.value
    assert resposta.json()["tipo"] == TipoMaterial.PDF.value


@pytest.mark.asyncio
async def test_upload_com_tipo_de_arquivo_invalido_retorna_415(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "mat3@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)

    resposta = await cliente.post(
        f"/disciplinas/{disciplina_id}/materiais",
        data={"titulo": "Arquivo errado"},
        files={"arquivo": ("imagem.png", b"nao e um pdf", "image/png")},
        headers=cabecalhos,
    )

    assert resposta.status_code == 415


@pytest.mark.asyncio
async def test_upload_com_content_type_pdf_mas_sem_assinatura_real_retorna_415(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "mat3b@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)

    resposta = await cliente.post(
        f"/disciplinas/{disciplina_id}/materiais",
        data={"titulo": "Disfarçado de PDF"},
        files={"arquivo": ("falso.pdf", b"isto nao comeca com a assinatura do pdf", "application/pdf")},
        headers=cabecalhos,
    )

    assert resposta.status_code == 415


@pytest.mark.asyncio
async def test_upload_de_texto_com_bytes_invalidos_em_utf8_retorna_415(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "mat3c@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)

    resposta = await cliente.post(
        f"/disciplinas/{disciplina_id}/materiais",
        data={"titulo": "Texto corrompido"},
        files={"arquivo_texto": ("ruim.txt", b"\xff\xfe\x00\x01", "text/plain")},
        headers=cabecalhos,
    )

    assert resposta.status_code == 415


@pytest.mark.asyncio
async def test_upload_de_texto_acima_do_limite_retorna_413(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "mat4@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    texto_enorme = "a" * (10 * 1024 * 1024 + 1)

    resposta = await enviar_material_texto(cliente, disciplina_id, cabecalhos, "Texto enorme", texto_enorme)

    assert resposta.status_code == 413


@pytest.mark.asyncio
async def test_listar_obter_e_remover_material(cliente):
    cabecalhos = await cadastrar_e_logar(cliente, "mat5@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos)
    criado = await enviar_material_texto(cliente, disciplina_id, cabecalhos, "Material", "Texto simples")
    material_id = criado.json()["id"]

    lista = await cliente.get(f"/disciplinas/{disciplina_id}/materiais", headers=cabecalhos)
    assert lista.status_code == 200
    assert len(lista.json()) == 1

    obtido = await cliente.get(f"/materiais/{material_id}", headers=cabecalhos)
    assert obtido.status_code == 200

    removido = await cliente.delete(f"/materiais/{material_id}", headers=cabecalhos)
    assert removido.status_code == 204

    buscado = await cliente.get(f"/materiais/{material_id}", headers=cabecalhos)
    assert buscado.status_code == 404


@pytest.mark.asyncio
async def test_material_de_outro_usuario_retorna_404(cliente):
    cabecalhos_a = await cadastrar_e_logar(cliente, "mat6@exemplo.com")
    cabecalhos_b = await cadastrar_e_logar(cliente, "mat7@exemplo.com")
    disciplina_id = await criar_disciplina(cliente, cabecalhos_a)
    criado = await enviar_material_texto(cliente, disciplina_id, cabecalhos_a, "Material privado", "Segredo")
    material_id = criado.json()["id"]

    resposta = await cliente.get(f"/materiais/{material_id}", headers=cabecalhos_b)

    assert resposta.status_code == 404
