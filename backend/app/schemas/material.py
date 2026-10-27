from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.material import StatusMaterial, TipoMaterial


class MaterialResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    disciplina_id: int
    titulo: str
    tipo: TipoMaterial
    status: StatusMaterial
    resumo: str | None
    criado_em: datetime
