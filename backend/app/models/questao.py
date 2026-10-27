from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.simulado import Simulado


class Questao(Base):
    __tablename__ = "questoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    simulado_id: Mapped[int] = mapped_column(
        ForeignKey("simulados.id", ondelete="CASCADE"), nullable=False, index=True
    )
    enunciado: Mapped[str] = mapped_column(Text, nullable=False)
    alternativas: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    correta: Mapped[int] = mapped_column(Integer, nullable=False)
    explicacao: Mapped[str] = mapped_column(Text, nullable=False)
    trecho_id: Mapped[int | None] = mapped_column(
        ForeignKey("trechos.id", ondelete="SET NULL"), nullable=True
    )

    simulado: Mapped["Simulado"] = relationship(back_populates="questoes")
