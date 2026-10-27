from fastapi import APIRouter, Depends, status

from app.dependencies import RepositorioUsuario, UsuarioAtual, limitar_taxa_auth
from app.schemas.token import Token
from app.schemas.usuario import UsuarioCadastro, UsuarioLogin, UsuarioResposta
from app.services.autenticacao_servico import AutenticacaoServico

router = APIRouter(prefix="/auth", tags=["autenticacao"])


@router.post(
    "/cadastro",
    response_model=UsuarioResposta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(limitar_taxa_auth)],
)
async def cadastrar(dados: UsuarioCadastro, repositorio: RepositorioUsuario) -> UsuarioResposta:
    servico = AutenticacaoServico(repositorio)
    usuario = await servico.cadastrar(dados)
    return UsuarioResposta.model_validate(usuario)


@router.post("/login", response_model=Token, dependencies=[Depends(limitar_taxa_auth)])
async def login(dados: UsuarioLogin, repositorio: RepositorioUsuario) -> Token:
    servico = AutenticacaoServico(repositorio)
    token = await servico.autenticar(dados)
    return Token(access_token=token)


@router.get("/eu", response_model=UsuarioResposta)
async def eu(usuario: UsuarioAtual) -> UsuarioResposta:
    return UsuarioResposta.model_validate(usuario)
