from pydantic import BaseModel


class RespostaSaude(BaseModel):
    status: str
    banco: str
