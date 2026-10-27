from fastapi import APIRouter, Depends, status

from app.core.erros import ErroAplicacao
from app.dependencies import (
    ProvedorTexto,
    RepositorioMaterial,
    RepositorioSimulado,
    RepositorioTrecho,
    UsuarioAtual,
    verificar_limite_ia,
)
from app.schemas.simulado import CorrecaoCriacao, CorrecaoResposta, SimuladoCriacao, SimuladoResposta
from app.services.simulado_servico import SimuladoServico

router = APIRouter(tags=["simulados"])


@router.post(
    "/materiais/{material_id}/simulados",
    response_model=SimuladoResposta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verificar_limite_ia)],
)
async def gerar_simulado(
    material_id: int,
    dados: SimuladoCriacao,
    usuario: UsuarioAtual,
    repositorio_simulado: RepositorioSimulado,
    repositorio_trecho: RepositorioTrecho,
    repositorio_material: RepositorioMaterial,
    provedor_texto: ProvedorTexto,
) -> SimuladoResposta:
    servico = SimuladoServico(repositorio_simulado, repositorio_trecho, repositorio_material, provedor_texto)
    simulado = await servico.gerar(material_id, usuario.id, dados.quantidade)
    return SimuladoResposta.model_validate(simulado)


@router.get("/simulados/{simulado_id}", response_model=SimuladoResposta)
async def obter_simulado(
    simulado_id: int, usuario: UsuarioAtual, repositorio_simulado: RepositorioSimulado
) -> SimuladoResposta:
    simulado = await repositorio_simulado.buscar_por_id_e_usuario(simulado_id, usuario.id)
    if simulado is None:
        raise ErroAplicacao("Simulado não encontrado", status_code=404)
    return SimuladoResposta.model_validate(simulado)


@router.post("/simulados/{simulado_id}/corrigir", response_model=CorrecaoResposta)
async def corrigir_simulado_endpoint(
    simulado_id: int,
    dados: CorrecaoCriacao,
    usuario: UsuarioAtual,
    repositorio_simulado: RepositorioSimulado,
    repositorio_trecho: RepositorioTrecho,
    repositorio_material: RepositorioMaterial,
    provedor_texto: ProvedorTexto,
) -> CorrecaoResposta:
    servico = SimuladoServico(repositorio_simulado, repositorio_trecho, repositorio_material, provedor_texto)
    respostas = [(item.questao_id, item.alternativa) for item in dados.respostas]
    return await servico.corrigir(simulado_id, usuario.id, respostas)
