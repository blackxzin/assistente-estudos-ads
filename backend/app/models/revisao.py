import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class StatusRevisao(enum.StrEnum):
    PENDENTE = "pendente"
    FEITA = "feita"
    PULADA = "pulada"


class Revisao(Base):
    __tablename__ = "revisoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materiais.id", ondelete="CASCADE"), nullable=False, index=True
    )
    data_prevista: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    etapa: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[StatusRevisao] = mapped_column(
        Enum(
            StatusRevisao,
            name="status_revisao",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        default=StatusRevisao.PENDENTE,
    )
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
