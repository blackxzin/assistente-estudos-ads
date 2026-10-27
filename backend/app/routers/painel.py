from fastapi import APIRouter

from app.dependencies import RepositorioPrazo, RepositorioRevisao, RepositorioSimulado, UsuarioAtual
from app.schemas.painel import PainelResposta
from app.services.painel_servico import PainelServico

router = APIRouter(tags=["painel"])


@router.get("/painel", response_model=PainelResposta)
async def obter_painel(
    usuario: UsuarioAtual,
    repositorio_prazo: RepositorioPrazo,
    repositorio_revisao: RepositorioRevisao,
    repositorio_simulado: RepositorioSimulado,
) -> PainelResposta:
    servico = PainelServico(repositorio_prazo, repositorio_revisao, repositorio_simulado)
    return await servico.montar(usuario.id)
