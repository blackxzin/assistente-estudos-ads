from app.config import configuracoes
from app.ia.provedor import ProvedorIA
from app.ia.provedor_anthropic import ProvedorAnthropic
from app.ia.provedor_falso import ProvedorFalso
from app.ia.provedor_openai import ProvedorOpenAI


def obter_provedor_texto() -> ProvedorIA:
    """Fábrica do provedor de geração de texto, escolhido via IA_PROVEDOR."""
    if configuracoes.IA_PROVEDOR == "falso":
        return ProvedorFalso(configuracoes.EMBEDDING_DIM)
    if configuracoes.IA_PROVEDOR == "anthropic":
        return ProvedorAnthropic(configuracoes.IA_API_KEY)
    return ProvedorOpenAI(configuracoes.IA_API_KEY)


def obter_provedor_embedding() -> ProvedorIA:
    """Fábrica do provedor de embeddings, escolhido via EMBEDDING_PROVEDOR (Anthropic não tem)."""
    if configuracoes.EMBEDDING_PROVEDOR == "falso":
        return ProvedorFalso(configuracoes.EMBEDDING_DIM)
    return ProvedorOpenAI(configuracoes.IA_API_KEY)
