import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.disciplina import Disciplina


class TipoPrazo(enum.StrEnum):
    PROVA = "prova"
    TRABALHO = "trabalho"


class Prazo(Base):
    __tablename__ = "prazos"

    id: Mapped[int] = mapped_column(primary_key=True)
    disciplina_id: Mapped[int] = mapped_column(
        ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo: Mapped[TipoPrazo] = mapped_column(
        Enum(TipoPrazo, name="tipo_prazo", values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable=False,
    )
    data: Mapped[date] = mapped_column(Date, nullable=False)
    concluido: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    disciplina: Mapped["Disciplina"] = relationship(back_populates="prazos")
