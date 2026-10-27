from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.prazo import Prazo


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    professor: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cor: Mapped[str | None] = mapped_column(String(7), nullable=True)

    prazos: Mapped[list["Prazo"]] = relationship(
        back_populates="disciplina", cascade="all, delete-orphan"
    )
