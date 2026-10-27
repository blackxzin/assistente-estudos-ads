from fastapi import APIRouter, status

from app.dependencies import (
    RepositorioDisciplina,
    RepositorioMaterial,
    RepositorioPrazo,
    RepositorioRevisao,
    UsuarioAtual,
)
from app.models.prazo import TipoPrazo
from app.schemas.disciplina import DisciplinaAtualizacao, DisciplinaCriacao, DisciplinaResposta
from app.schemas.prazo import PrazoCriacao, PrazoResposta
from app.services.disciplina_servico import DisciplinaServico
from app.services.prazo_servico import PrazoServico
from app.services.revisao_servico import RevisaoServico

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])


@router.post("", response_model=DisciplinaResposta, status_code=status.HTTP_201_CREATED)
async def criar_disciplina(
    dados: DisciplinaCriacao, usuario: UsuarioAtual, repositorio: RepositorioDisciplina
) -> DisciplinaResposta:
    servico = DisciplinaServico(repositorio)
    disciplina = await servico.criar(usuario.id, dados)
    return DisciplinaResposta.model_validate(disciplina)


@router.get("", response_model=list[DisciplinaResposta])
async def listar_disciplinas(
    usuario: UsuarioAtual, repositorio: RepositorioDisciplina
) -> list[DisciplinaResposta]:
    servico = DisciplinaServico(repositorio)
    disciplinas = await servico.listar(usuario.id)
    return [DisciplinaResposta.model_validate(disciplina) for disciplina in disciplinas]


@router.get("/{disciplina_id}", response_model=DisciplinaResposta)
async def obter_disciplina(
    disciplina_id: int, usuario: UsuarioAtual, repositorio: RepositorioDisciplina
) -> DisciplinaResposta:
    servico = DisciplinaServico(repositorio)
    disciplina = await servico.obter(disciplina_id, usuario.id)
    return DisciplinaResposta.model_validate(disciplina)


@router.put("/{disciplina_id}", response_model=DisciplinaResposta)
async def atualizar_disciplina(
    disciplina_id: int,
    dados: DisciplinaAtualizacao,
    usuario: UsuarioAtual,
    repositorio: RepositorioDisciplina,
) -> DisciplinaResposta:
    servico = DisciplinaServico(repositorio)
    disciplina = await servico.atualizar(disciplina_id, usuario.id, dados)
    return DisciplinaResposta.model_validate(disciplina)


@router.delete("/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_disciplina(
    disciplina_id: int, usuario: UsuarioAtual, repositorio: RepositorioDisciplina
) -> None:
    servico = DisciplinaServico(repositorio)
    await servico.remover(disciplina_id, usuario.id)


@router.post("/{disciplina_id}/prazos", response_model=PrazoResposta, status_code=status.HTTP_201_CREATED)
async def criar_prazo(
    disciplina_id: int,
    dados: PrazoCriacao,
    usuario: UsuarioAtual,
    repositorio: RepositorioPrazo,
    repositorio_disciplina: RepositorioDisciplina,
    repositorio_revisao: RepositorioRevisao,
    repositorio_material: RepositorioMaterial,
) -> PrazoResposta:
    servico = PrazoServico(repositorio, repositorio_disciplina)
    prazo = await servico.criar(disciplina_id, usuario.id, dados)

    if prazo.tipo == TipoPrazo.PROVA:
        revisao_servico = RevisaoServico(repositorio_revisao, repositorio, repositorio_material)
        await revisao_servico.reagendar_pendentes_da_disciplina(disciplina_id)

    return PrazoResposta.model_validate(prazo)


@router.get("/{disciplina_id}/prazos", response_model=list[PrazoResposta])
async def listar_prazos(
    disciplina_id: int,
    usuario: UsuarioAtual,
    repositorio: RepositorioPrazo,
    repositorio_disciplina: RepositorioDisciplina,
) -> list[PrazoResposta]:
    servico = PrazoServico(repositorio, repositorio_disciplina)
    prazos = await servico.listar(disciplina_id, usuario.id)
    return [PrazoResposta.model_validate(prazo) for prazo in prazos]
