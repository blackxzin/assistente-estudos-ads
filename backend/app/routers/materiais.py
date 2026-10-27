from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.config import configuracoes
from app.core.erros import ArquivoMuitoGrande, ErroAplicacao, TipoArquivoInvalido
from app.dependencies import (
    ProvedorEmbedding,
    ProvedorTexto,
    RepositorioDisciplina,
    RepositorioMaterial,
    RepositorioPrazo,
    RepositorioRevisao,
    RepositorioTrecho,
    UsuarioAtual,
    verificar_limite_ia,
)
from app.models.material import StatusMaterial
from app.schemas.material import MaterialResposta
from app.schemas.pergunta import PerguntaCriacao, RespostaPergunta
from app.services.material_servico import MaterialServico
from app.services.qa_servico import QAServico
from app.services.resumo_servico import ResumoServico
from app.services.revisao_servico import RevisaoServico
from app.services.validacao_arquivo import decodificar_texto_utf8, eh_pdf_valido

router = APIRouter(tags=["materiais"])


def _tamanho_maximo_bytes() -> int:
    return configuracoes.TAMANHO_MAXIMO_ARQUIVO_MB * 1024 * 1024


@router.post(
    "/disciplinas/{disciplina_id}/materiais",
    response_model=MaterialResposta,
    status_code=status.HTTP_201_CREATED,
)
async def enviar_material(
    disciplina_id: int,
    usuario: UsuarioAtual,
    repositorio_material: RepositorioMaterial,
    repositorio_trecho: RepositorioTrecho,
    repositorio_disciplina: RepositorioDisciplina,
    repositorio_revisao: RepositorioRevisao,
    repositorio_prazo: RepositorioPrazo,
    provedor_embedding: ProvedorEmbedding,
    titulo: str = Form(...),
    arquivo: UploadFile | None = File(None),
    arquivo_texto: UploadFile | None = File(None),
) -> MaterialResposta:
    servico = MaterialServico(
        repositorio_material, repositorio_trecho, repositorio_disciplina, provedor_embedding
    )

    if arquivo is not None:
        if arquivo.content_type != "application/pdf":
            raise TipoArquivoInvalido("Envie um arquivo PDF (application/pdf) ou use o campo arquivo_texto")
        conteudo_bytes = await arquivo.read()
        if len(conteudo_bytes) > _tamanho_maximo_bytes():
            raise ArquivoMuitoGrande()
        if not eh_pdf_valido(conteudo_bytes):
            raise TipoArquivoInvalido("O arquivo não parece ser um PDF válido")
        material = await servico.criar_a_partir_de_pdf(disciplina_id, usuario.id, titulo, conteudo_bytes)
    elif arquivo_texto is not None:
        conteudo_bytes = await arquivo_texto.read()
        if len(conteudo_bytes) > _tamanho_maximo_bytes():
            raise ArquivoMuitoGrande()
        texto = decodificar_texto_utf8(conteudo_bytes)
        if texto is None:
            raise TipoArquivoInvalido("O arquivo de texto precisa estar em UTF-8")
        material = await servico.criar_a_partir_de_texto(disciplina_id, usuario.id, titulo, texto)
    else:
        raise ErroAplicacao("Envie um arquivo PDF ou o campo arquivo_texto", status_code=400)

    if material.status == StatusMaterial.PRONTO:
        revisao_servico = RevisaoServico(repositorio_revisao, repositorio_prazo, repositorio_material)
        await revisao_servico.agendar_inicial(material.id, disciplina_id)

    return MaterialResposta.model_validate(material)


@router.get("/disciplinas/{disciplina_id}/materiais", response_model=list[MaterialResposta])
async def listar_materiais(
    disciplina_id: int,
    usuario: UsuarioAtual,
    repositorio_material: RepositorioMaterial,
    repositorio_disciplina: RepositorioDisciplina,
) -> list[MaterialResposta]:
    servico = MaterialServico(repositorio_material, repositorio_disciplina=repositorio_disciplina)
    materiais = await servico.listar(disciplina_id, usuario.id)
    return [MaterialResposta.model_validate(material) for material in materiais]


@router.get("/materiais/{material_id}", response_model=MaterialResposta)
async def obter_material(
    material_id: int, usuario: UsuarioAtual, repositorio_material: RepositorioMaterial
) -> MaterialResposta:
    servico = MaterialServico(repositorio_material)
    material = await servico.obter(material_id, usuario.id)
    return MaterialResposta.model_validate(material)


@router.delete("/materiais/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_material(
    material_id: int, usuario: UsuarioAtual, repositorio_material: RepositorioMaterial
) -> None:
    servico = MaterialServico(repositorio_material)
    await servico.remover(material_id, usuario.id)


@router.post(
    "/materiais/{material_id}/perguntas",
    response_model=RespostaPergunta,
    dependencies=[Depends(verificar_limite_ia)],
)
async def perguntar(
    material_id: int,
    dados: PerguntaCriacao,
    usuario: UsuarioAtual,
    repositorio_material: RepositorioMaterial,
    repositorio_trecho: RepositorioTrecho,
    provedor_embedding: ProvedorEmbedding,
    provedor_texto: ProvedorTexto,
) -> RespostaPergunta:
    servico = QAServico(repositorio_trecho, repositorio_material, provedor_embedding, provedor_texto)
    return await servico.perguntar(material_id, usuario.id, dados.pergunta)


@router.post(
    "/materiais/{material_id}/resumo",
    response_model=MaterialResposta,
    dependencies=[Depends(verificar_limite_ia)],
)
async def gerar_resumo(
    material_id: int,
    usuario: UsuarioAtual,
    repositorio_material: RepositorioMaterial,
    repositorio_trecho: RepositorioTrecho,
    provedor_texto: ProvedorTexto,
) -> MaterialResposta:
    servico = ResumoServico(repositorio_material, repositorio_trecho, provedor_texto)
    material = await servico.gerar_resumo(material_id, usuario.id)
    return MaterialResposta.model_validate(material)
