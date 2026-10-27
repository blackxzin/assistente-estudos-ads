from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SimuladoCriacao(BaseModel):
    quantidade: int = Field(default=5, ge=1, le=20)


class QuestaoResposta(BaseModel):
    """Questão sem gabarito, usada na criação e na consulta do simulado."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    enunciado: str
    alternativas: list[str]


class SimuladoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    material_id: int
    criado_em: datetime
    questoes: list[QuestaoResposta]


class RespostaItem(BaseModel):
    questao_id: int
    alternativa: int = Field(ge=0, le=3)


class CorrecaoCriacao(BaseModel):
    respostas: list[RespostaItem]


class ItemCorrecaoResposta(BaseModel):
    questao_id: int
    enunciado: str
    alternativas: list[str]
    escolhida: int | None
    correta: int
    acertou: bool
    explicacao: str
    trecho_id: int | None


class CorrecaoResposta(BaseModel):
    nota: float
    acertos: int
    total: int
    itens: list[ItemCorrecaoResposta]


class QuestaoGerada(BaseModel):
    """Formato exigido do LLM ao gerar uma questão; valida a saída antes de persistir."""

    enunciado: str = Field(min_length=1)
    alternativas: list[str] = Field(min_length=4, max_length=4)
    correta: int = Field(ge=0, le=3)
    explicacao: str = Field(min_length=1)
    trecho_id: int | None = None


class SimuladoGerado(BaseModel):
    questoes: list[QuestaoGerada]
