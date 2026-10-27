from app.core.erros import ConflitoDeDados, NaoAutorizado
from app.core.seguranca import criar_token_acesso, gerar_hash_senha, verificar_senha
from app.models.usuario import Usuario
from app.repositories.usuario_repositorio import UsuarioRepositorio
from app.schemas.usuario import UsuarioCadastro, UsuarioLogin

_HASH_FALSO = gerar_hash_senha("senha-usada-apenas-para-igualar-o-tempo-de-resposta")


class AutenticacaoServico:
    def __init__(self, repositorio: UsuarioRepositorio):
        self.repositorio = repositorio

    async def cadastrar(self, dados: UsuarioCadastro) -> Usuario:
        usuario_existente = await self.repositorio.buscar_por_email(dados.email)
        if usuario_existente is not None:
            raise ConflitoDeDados("Email já cadastrado")

        senha_hash = gerar_hash_senha(dados.senha)
        return await self.repositorio.criar(nome=dados.nome, email=dados.email, senha_hash=senha_hash)

    async def autenticar(self, dados: UsuarioLogin) -> str:
        usuario = await self.repositorio.buscar_por_email(dados.email)

        # Sempre roda o verificar_senha (mesmo sem usuário) para não expor, pelo tempo de
        # resposta, se um e-mail está cadastrado ou não.
        hash_para_comparar = usuario.senha_hash if usuario is not None else _HASH_FALSO
        senha_valida = verificar_senha(dados.senha, hash_para_comparar)

        if usuario is None or not senha_valida:
            raise NaoAutorizado("Email ou senha inválidos")

        return criar_token_acesso(usuario.id)
