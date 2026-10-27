from datetime import date
from typing import Literal

from pydantic import BaseModel

from app.models.revisao import StatusRevisao


class RevisaoResposta(BaseModel):
    id: int
    material_id: int
    material_titulo: str
    disciplina_nome: str
    data_prevista: date
    etapa: int
    status: StatusRevisao


class ConclusaoRevisaoCriacao(BaseModel):
    desempenho: Literal["lembrei", "dificil", "esqueci"]
