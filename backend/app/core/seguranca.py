from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.config import configuracoes

ALGORITMO_JWT = "HS256"
MINUTOS_EXPIRACAO_TOKEN = 60 * 24


def gerar_hash_senha(senha: str) -> str:
    """Gera o hash bcrypt de uma senha em texto plano."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """Confere se a senha em texto plano corresponde ao hash armazenado."""
    return bcrypt.checkpw(senha.encode("utf-8"), hash_senha.encode("utf-8"))


def criar_token_acesso(usuario_id: int) -> str:
    """Gera um JWT com expiração contendo o id do usuário."""
    expira_em = datetime.now(UTC) + timedelta(minutes=MINUTOS_EXPIRACAO_TOKEN)
    payload = {"sub": str(usuario_id), "exp": expira_em}
    return jwt.encode(payload, configuracoes.JWT_SECRET, algorithm=ALGORITMO_JWT)


def decodificar_token(token: str) -> int:
    """Decodifica o JWT e retorna o id do usuário. Lança jwt.PyJWTError se inválido/expirado."""
    payload = jwt.decode(token, configuracoes.JWT_SECRET, algorithms=[ALGORITMO_JWT])
    return int(payload["sub"])
