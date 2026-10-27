"""cria tabela uso_ia

Revision ID: 0007
Revises: 0006
Create Date: 2026-10-27

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0007"
down_revision: str | None = "0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "uso_ia",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "usuario_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("data", sa.Date(), nullable=False, index=True),
        sa.Column("contagem", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("usuario_id", "data", name="uq_uso_ia_usuario_data"),
    )


def downgrade() -> None:
    op.drop_table("uso_ia")
