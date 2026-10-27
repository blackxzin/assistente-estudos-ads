import pytest

from app.config import Configuracoes


def test_jwt_secret_fraco_em_producao_e_rejeitado():
    with pytest.raises(ValueError, match="JWT_SECRET"):
        Configuracoes(
            DATABASE_URL="postgresql+asyncpg://x:x@localhost/x",
            JWT_SECRET="curto",
            AMBIENTE="production",
        )


def test_jwt_secret_forte_em_producao_e_aceito():
    configuracoes = Configuracoes(
        DATABASE_URL="postgresql+asyncpg://x:x@localhost/x",
        JWT_SECRET="a" * 32,
        AMBIENTE="production",
    )

    assert configuracoes.JWT_SECRET == "a" * 32


def test_jwt_secret_fraco_em_desenvolvimento_e_aceito():
    configuracoes = Configuracoes(
        DATABASE_URL="postgresql+asyncpg://x:x@localhost/x",
        JWT_SECRET="curto",
        AMBIENTE="development",
    )

    assert configuracoes.JWT_SECRET == "curto"


def test_origens_cors_separa_por_virgula_e_remove_espacos():
    configuracoes = Configuracoes(
        DATABASE_URL="postgresql+asyncpg://x:x@localhost/x",
        JWT_SECRET="segredo",
        CORS_ORIGINS="http://a.com, http://b.com ,,",
    )

    assert configuracoes.origens_cors == ["http://a.com", "http://b.com"]
