from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.prazo import TipoPrazo


class PrazoCriacao(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    tipo: TipoPrazo
    data: date


class PrazoAtualizacao(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=200)
    tipo: TipoPrazo | None = None
    data: date | None = None
    concluido: bool | None = None


class PrazoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    disciplina_id: int
    titulo: str
    tipo: TipoPrazo
    data: date
    concluido: bool
