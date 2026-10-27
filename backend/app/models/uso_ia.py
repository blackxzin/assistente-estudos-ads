from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UsoIA(Base):
    __tablename__ = "uso_ia"
    __table_args__ = (UniqueConstraint("usuario_id", "data", name="uq_uso_ia_usuario_data"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    data: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    contagem: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
