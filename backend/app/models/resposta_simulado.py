from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RespostaSimulado(Base):
    __tablename__ = "respostas_simulado"

    id: Mapped[int] = mapped_column(primary_key=True)
    questao_id: Mapped[int] = mapped_column(
        ForeignKey("questoes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    alternativa_escolhida: Mapped[int | None] = mapped_column(Integer, nullable=True)
    acertou: Mapped[bool] = mapped_column(Boolean, nullable=False)
