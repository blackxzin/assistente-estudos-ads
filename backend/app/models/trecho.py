from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import configuracoes
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.material import Material


class Trecho(Base):
    __tablename__ = "trechos"

    id: Mapped[int] = mapped_column(primary_key=True)
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materiais.id", ondelete="CASCADE"), nullable=False, index=True
    )
    conteudo: Mapped[str] = mapped_column(Text, nullable=False)
    pagina: Mapped[int | None] = mapped_column(Integer, nullable=True)
    posicao: Mapped[int] = mapped_column(Integer, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(configuracoes.EMBEDDING_DIM), nullable=False)

    material: Mapped["Material"] = relationship(back_populates="trechos")
