from pydantic import BaseModel, Field


class PerguntaCriacao(BaseModel):
    pergunta: str = Field(min_length=1, max_length=2000)


class CitacaoResposta(BaseModel):
    trecho_id: int
    pagina: int | None
    trecho: str


class RespostaPergunta(BaseModel):
    resposta: str
    citacoes: list[CitacaoResposta]
