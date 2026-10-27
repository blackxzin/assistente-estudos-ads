from fastapi import APIRouter, status

from app.dependencies import (
    RepositorioDisciplina,
    RepositorioMaterial,
    RepositorioPrazo,
    RepositorioRevisao,
    UsuarioAtual,
)
from app.models.prazo import TipoPrazo
from app.schemas.prazo import PrazoAtualizacao, PrazoResposta
from app.services.prazo_servico import PrazoServico
from app.services.revisao_servico import RevisaoServico

router = APIRouter(prefix="/prazos", tags=["prazos"])


@router.put("/{prazo_id}", response_model=PrazoResposta)
async def atualizar_prazo(
    prazo_id: int,
    dados: PrazoAtualizacao,
    usuario: UsuarioAtual,
    repositorio: RepositorioPrazo,
    repositorio_disciplina: RepositorioDisciplina,
    repositorio_revisao: RepositorioRevisao,
    repositorio_material: RepositorioMaterial,
) -> PrazoResposta:
    servico = PrazoServico(repositorio, repositorio_disciplina)
    prazo = await servico.atualizar(prazo_id, usuario.id, dados)

    if prazo.tipo == TipoPrazo.PROVA:
        revisao_servico = RevisaoServico(repositorio_revisao, repositorio, repositorio_material)
        await revisao_servico.reagendar_pendentes_da_disciplina(prazo.disciplina_id)

    return PrazoResposta.model_validate(prazo)


@router.delete("/{prazo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_prazo(
    prazo_id: int,
    usuario: UsuarioAtual,
    repositorio: RepositorioPrazo,
    repositorio_disciplina: RepositorioDisciplina,
) -> None:
    servico = PrazoServico(repositorio, repositorio_disciplina)
    await servico.remover(prazo_id, usuario.id)
