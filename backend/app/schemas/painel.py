from datetime import date

from pydantic import BaseModel

from app.models.prazo import TipoPrazo
from app.schemas.revisao import RevisaoResposta


class PrazoPainelResposta(BaseModel):
    id: int
    titulo: str
    tipo: TipoPrazo
    data: date
    disciplina_nome: str


class UltimoSimuladoResposta(BaseModel):
    simulado_id: int
    material_titulo: str
    nota: float
    data: date


class DesempenhoResposta(BaseModel):
    media_nota: float | None
    total_simulados: int
    ultimos: list[UltimoSimuladoResposta]


class PainelResposta(BaseModel):
    proximos_prazos: list[PrazoPainelResposta]
    revisoes_hoje: list[RevisaoResposta]
    desempenho: DesempenhoResposta
