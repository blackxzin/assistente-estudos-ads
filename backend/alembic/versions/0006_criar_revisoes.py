"""cria tabela revisoes

Revision ID: 0006
Revises: 0005
Create Date: 2026-10-27

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

status_revisao = sa.Enum("pendente", "feita", "pulada", name="status_revisao", create_type=False)


def upgrade() -> None:
    status_revisao.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "revisoes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "material_id",
            sa.Integer(),
            sa.ForeignKey("materiais.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("data_prevista", sa.Date(), nullable=False, index=True),
        sa.Column("etapa", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", status_revisao, nullable=False, server_default="pendente"),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("revisoes")
    status_revisao.drop(op.get_bind(), checkfirst=True)
