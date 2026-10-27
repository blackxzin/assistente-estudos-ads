from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

TAMANHO_MINIMO_JWT_SECRET_PRODUCAO = 32


class Configuracoes(BaseSettings):
    """Configurações da aplicação, lidas do ambiente (.env)."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str
    JWT_SECRET: str
    IA_PROVEDOR: str = "openai"
    IA_API_KEY: str = ""
    EMBEDDING_PROVEDOR: str = "openai"
    EMBEDDING_DIM: int = 1536
    TAMANHO_TRECHO: int = 1000
    SOBREPOSICAO_TRECHO: int = 200
    TOP_K_BUSCA: int = 5
    LIMIAR_SIMILARIDADE: float = 0.75
    TAMANHO_MAXIMO_ARQUIVO_MB: int = 10
    LIMITE_IA_DIARIO: int = 20
    CORS_ORIGINS: str = "http://localhost:3000"
    RATE_LIMIT_JANELA_SEGUNDOS: int = 60
    RATE_LIMIT_MAX_REQUISICOES: int = 10
    AMBIENTE: str = "development"

    @model_validator(mode="after")
    def _validar_jwt_secret_em_producao(self) -> "Configuracoes":
        if self.AMBIENTE == "production" and len(self.JWT_SECRET) < TAMANHO_MINIMO_JWT_SECRET_PRODUCAO:
            raise ValueError(
                "JWT_SECRET precisa ter pelo menos "
                f"{TAMANHO_MINIMO_JWT_SECRET_PRODUCAO} caracteres em produção"
            )
        return self

    @property
    def origens_cors(self) -> list[str]:
        return [origem.strip() for origem in self.CORS_ORIGINS.split(",") if origem.strip()]


configuracoes = Configuracoes()
