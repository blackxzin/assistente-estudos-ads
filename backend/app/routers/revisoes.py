from datetime import date

from fastapi import APIRouter

from app.core.erros import ErroAplicacao
from app.dependencies import (
    RepositorioDisciplina,
    RepositorioMaterial,
    RepositorioPrazo,
    RepositorioRevisao,
    UsuarioAtual,
)
from app.schemas.revisao import ConclusaoRevisaoCriacao, RevisaoResposta
from app.services.revisao_servico import RevisaoServico

router = APIRouter(tags=["revisoes"])


@router.get("/revisoes", response_model=list[RevisaoResposta])
async def listar_revisoes(
    de: date, ate: date, usuario: UsuarioAtual, repositorio_revisao: RepositorioRevisao
) -> list[RevisaoResposta]:
    if de > ate:
        raise ErroAplicacao("O período informado é inválido: 'de' deve ser anterior ou igual a 'ate'")

    linhas = await repositorio_revisao.listar_por_usuario_no_periodo(usuario.id, de, ate)
    return [
        RevisaoResposta(
            id=revisao.id,
            material_id=revisao.material_id,
            material_titulo=titulo,
            disciplina_nome=nome,
            data_prevista=revisao.data_prevista,
            etapa=revisao.etapa,
            status=revisao.status,
        )
        for revisao, titulo, nome in linhas
    ]


@router.post("/revisoes/{revisao_id}/concluir", response_model=RevisaoResposta)
async def concluir_revisao(
    revisao_id: int,
    dados: ConclusaoRevisaoCriacao,
    usuario: UsuarioAtual,
    repositorio_revisao: RepositorioRevisao,
    repositorio_prazo: RepositorioPrazo,
    repositorio_material: RepositorioMaterial,
    repositorio_disciplina: RepositorioDisciplina,
) -> RevisaoResposta:
    servico = RevisaoServico(repositorio_revisao, repositorio_prazo, repositorio_material)
    revisao = await servico.concluir(revisao_id, usuario.id, dados.desempenho)

    material = await repositorio_material.buscar_por_id(revisao.material_id)
    disciplina = await repositorio_disciplina.buscar_por_id_e_usuario(material.disciplina_id, usuario.id)
    return RevisaoResposta(
        id=revisao.id,
        material_id=revisao.material_id,
        material_titulo=material.titulo,
        disciplina_nome=disciplina.nome,
        data_prevista=revisao.data_prevista,
        etapa=revisao.etapa,
        status=revisao.status,
    )
