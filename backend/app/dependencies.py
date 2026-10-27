from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import limite_taxa
from app.core.erros import NaoAutorizado
from app.core.seguranca import decodificar_token
from app.database import obter_sessao
from app.ia.fabrica import obter_provedor_embedding, obter_provedor_texto
from app.ia.provedor import ProvedorIA
from app.models.usuario import Usuario
from app.repositories.disciplina_repositorio import DisciplinaRepositorio
from app.repositories.material_repositorio import MaterialRepositorio
from app.repositories.prazo_repositorio import PrazoRepositorio
from app.repositories.revisao_repositorio import RevisaoRepositorio
from app.repositories.simulado_repositorio import SimuladoRepositorio
from app.repositories.trecho_repositorio import TrechoRepositorio
from app.repositories.uso_ia_repositorio import UsoIARepositorio
from app.repositories.usuario_repositorio import UsuarioRepositorio
from app.services.limite_ia_servico import LimiteIAServico

SessaoBanco = Annotated[AsyncSession, Depends(obter_sessao)]


def obter_repositorio_usuario(sessao: SessaoBanco) -> UsuarioRepositorio:
    return UsuarioRepositorio(sessao)


def obter_repositorio_disciplina(sessao: SessaoBanco) -> DisciplinaRepositorio:
    return DisciplinaRepositorio(sessao)


def obter_repositorio_prazo(sessao: SessaoBanco) -> PrazoRepositorio:
    return PrazoRepositorio(sessao)


def obter_repositorio_material(sessao: SessaoBanco) -> MaterialRepositorio:
    return MaterialRepositorio(sessao)


def obter_repositorio_trecho(sessao: SessaoBanco) -> TrechoRepositorio:
    return TrechoRepositorio(sessao)


def obter_repositorio_simulado(sessao: SessaoBanco) -> SimuladoRepositorio:
    return SimuladoRepositorio(sessao)


def obter_repositorio_revisao(sessao: SessaoBanco) -> RevisaoRepositorio:
    return RevisaoRepositorio(sessao)


def obter_repositorio_uso_ia(sessao: SessaoBanco) -> UsoIARepositorio:
    return UsoIARepositorio(sessao)


RepositorioUsuario = Annotated[UsuarioRepositorio, Depends(obter_repositorio_usuario)]
RepositorioDisciplina = Annotated[DisciplinaRepositorio, Depends(obter_repositorio_disciplina)]
RepositorioPrazo = Annotated[PrazoRepositorio, Depends(obter_repositorio_prazo)]
RepositorioMaterial = Annotated[MaterialRepositorio, Depends(obter_repositorio_material)]
RepositorioTrecho = Annotated[TrechoRepositorio, Depends(obter_repositorio_trecho)]
RepositorioSimulado = Annotated[SimuladoRepositorio, Depends(obter_repositorio_simulado)]
RepositorioRevisao = Annotated[RevisaoRepositorio, Depends(obter_repositorio_revisao)]
RepositorioUsoIA = Annotated[UsoIARepositorio, Depends(obter_repositorio_uso_ia)]
ProvedorTexto = Annotated[ProvedorIA, Depends(obter_provedor_texto)]
ProvedorEmbedding = Annotated[ProvedorIA, Depends(obter_provedor_embedding)]

_esquema_bearer = HTTPBearer(auto_error=False)


async def usuario_atual(
    credenciais: Annotated[HTTPAuthorizationCredentials | None, Depends(_esquema_bearer)],
    repositorio: RepositorioUsuario,
) -> Usuario:
    """Resolve o usuário logado a partir do header Authorization: Bearer <token>."""
    if credenciais is None:
        raise NaoAutorizado("Token de acesso ausente")

    try:
        usuario_id = decodificar_token(credenciais.credentials)
    except Exception as erro:
        raise NaoAutorizado("Token de acesso inválido") from erro

    usuario = await repositorio.buscar_por_id(usuario_id)
    if usuario is None:
        raise NaoAutorizado("Usuário não encontrado")

    return usuario


UsuarioAtual = Annotated[Usuario, Depends(usuario_atual)]


async def verificar_limite_ia(usuario: UsuarioAtual, repositorio: RepositorioUsoIA) -> None:
    """Dependência a usar em todo endpoint que consome IA (resumo, perguntas, simulados)."""
    servico = LimiteIAServico(repositorio)
    await servico.verificar_e_registrar(usuario.id)


async def limitar_taxa_auth(request: Request) -> None:
    """Dependência a usar em /auth/login e /auth/cadastro, para limitar tentativas por IP."""
    chave = request.client.host if request.client else "desconhecido"
    limite_taxa.verificar_e_registrar(chave)
