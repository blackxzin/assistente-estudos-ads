from fastapi import APIRouter
from sqlalchemy import text

from app.dependencies import SessaoBanco
from app.schemas.saude import RespostaSaude

router = APIRouter()


@router.get("/saude", response_model=RespostaSaude)
async def verificar_saude(sessao: SessaoBanco) -> RespostaSaude:
    """Verifica se a API está no ar e se o banco responde."""
    try:
        await sessao.execute(text("SELECT 1"))
        banco_ok = True
    except Exception:
        banco_ok = False

    return RespostaSaude(
        status="ok" if banco_ok else "erro",
        banco="conectado" if banco_ok else "indisponivel",
    )
