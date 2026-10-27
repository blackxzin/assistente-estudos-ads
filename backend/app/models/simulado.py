from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.questao import Questao


class Simulado(Base):
    __tablename__ = "simulados"

    id: Mapped[int] = mapped_column(primary_key=True)
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materiais.id", ondelete="CASCADE"), nullable=False, index=True
    )
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    nota: Mapped[float | None] = mapped_column(Float, nullable=True)
    corrigido_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    questoes: Mapped[list["Questao"]] = relationship(
        back_populates="simulado", cascade="all, delete-orphan", order_by="Questao.id"
    )
