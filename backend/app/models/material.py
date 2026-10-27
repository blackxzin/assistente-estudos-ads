import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.trecho import Trecho


class TipoMaterial(enum.StrEnum):
    PDF = "pdf"
    TEXTO = "texto"


class StatusMaterial(enum.StrEnum):
    PROCESSANDO = "processando"
    PRONTO = "pronto"
    ERRO = "erro"


class Material(Base):
    __tablename__ = "materiais"

    id: Mapped[int] = mapped_column(primary_key=True)
    disciplina_id: Mapped[int] = mapped_column(
        ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo: Mapped[TipoMaterial] = mapped_column(
        Enum(
            TipoMaterial, name="tipo_material", values_callable=lambda enum_cls: [e.value for e in enum_cls]
        ),
        nullable=False,
    )
    status: Mapped[StatusMaterial] = mapped_column(
        Enum(
            StatusMaterial,
            name="status_material",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        default=StatusMaterial.PROCESSANDO,
    )
    resumo: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    trechos: Mapped[list["Trecho"]] = relationship(back_populates="material", cascade="all, delete-orphan")
