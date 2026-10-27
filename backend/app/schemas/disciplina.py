from pydantic import BaseModel, ConfigDict, Field

PADRAO_COR_HEX = r"^#[0-9A-Fa-f]{6}$"


class DisciplinaCriacao(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    professor: str | None = Field(default=None, max_length=120)
    cor: str | None = Field(default=None, pattern=PADRAO_COR_HEX)


class DisciplinaAtualizacao(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=120)
    professor: str | None = Field(default=None, max_length=120)
    cor: str | None = Field(default=None, pattern=PADRAO_COR_HEX)


class DisciplinaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    professor: str | None
    cor: str | None
