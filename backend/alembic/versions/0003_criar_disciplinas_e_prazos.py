"""cria disciplinas e prazos

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-27

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

tipo_prazo = sa.Enum("prova", "trabalho", name="tipo_prazo", create_type=False)


def upgrade() -> None:
    op.create_table(
        "disciplinas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "usuario_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("professor", sa.String(length=120), nullable=True),
        sa.Column("cor", sa.String(length=7), nullable=True),
    )

    tipo_prazo.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "prazos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "disciplina_id",
            sa.Integer(),
            sa.ForeignKey("disciplinas.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("tipo", tipo_prazo, nullable=False),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("concluido", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_table("prazos")
    tipo_prazo.drop(op.get_bind(), checkfirst=True)
    op.drop_table("disciplinas")
