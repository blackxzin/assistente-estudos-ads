import time
from collections import defaultdict

from app.config import configuracoes
from app.core.erros import MuitasRequisicoes

# Limitador de taxa simples, em memória do processo (janela deslizante por chave, ex.: IP).
# Funciona para uma única instância do backend. Com múltiplas instâncias (deploy escalado
# horizontalmente), cada processo teria sua própria contagem, então precisaria de um
# armazenamento compartilhado (ex.: Redis) para o limite valer globalmente.
_registros: dict[str, list[float]] = defaultdict(list)


def limpar_registros() -> None:
    """Zera o estado do limitador. Usado nos testes para isolar cada caso."""
    _registros.clear()


def verificar_e_registrar(chave: str) -> None:
    agora = time.monotonic()
    limite_inferior = agora - configuracoes.RATE_LIMIT_JANELA_SEGUNDOS
    marcacoes = _registros[chave]

    while marcacoes and marcacoes[0] < limite_inferior:
        marcacoes.pop(0)

    if len(marcacoes) >= configuracoes.RATE_LIMIT_MAX_REQUISICOES:
        raise MuitasRequisicoes()

    marcacoes.append(agora)
