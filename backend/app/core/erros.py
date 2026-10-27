from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ErroAplicacao(Exception):
    """Erro de negócio com mensagem e status HTTP próprios."""

    def __init__(self, mensagem: str, status_code: int = 400):
        self.mensagem = mensagem
        self.status_code = status_code


class NaoAutorizado(ErroAplicacao):
    def __init__(self, mensagem: str = "Credenciais inválidas"):
        super().__init__(mensagem, status_code=401)


class NaoEncontrado(ErroAplicacao):
    def __init__(self, mensagem: str = "Recurso não encontrado"):
        super().__init__(mensagem, status_code=404)


class ConflitoDeDados(ErroAplicacao):
    def __init__(self, mensagem: str = "Conflito de dados"):
        super().__init__(mensagem, status_code=409)


class ArquivoMuitoGrande(ErroAplicacao):
    def __init__(self, mensagem: str = "Arquivo excede o limite de tamanho permitido"):
        super().__init__(mensagem, status_code=413)


class TipoArquivoInvalido(ErroAplicacao):
    def __init__(self, mensagem: str = "Tipo de arquivo não suportado"):
        super().__init__(mensagem, status_code=415)


class LimiteIAExcedido(ErroAplicacao):
    def __init__(self, mensagem: str = "Limite diário de uso de IA atingido"):
        super().__init__(mensagem, status_code=429)


class MuitasRequisicoes(ErroAplicacao):
    def __init__(self, mensagem: str = "Muitas tentativas, tente novamente em instantes"):
        super().__init__(mensagem, status_code=429)


async def _tratar_erro_aplicacao(request: Request, exc: ErroAplicacao) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"erro": exc.mensagem})


def registrar_tratadores_de_erro(app: FastAPI) -> None:
    """Padroniza erros de negócio como JSON {"erro": "..."}."""
    app.add_exception_handler(ErroAplicacao, _tratar_erro_aplicacao)
