"""cria simulados, questoes e respostas_simulado

Revision ID: 0005
Revises: 0004
Create Date: 2026-10-27

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "simulados",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "material_id",
            sa.Integer(),
            sa.ForeignKey("materiais.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("nota", sa.Float(), nullable=True),
        sa.Column("corrigido_em", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "questoes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "simulado_id",
            sa.Integer(),
            sa.ForeignKey("simulados.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("enunciado", sa.Text(), nullable=False),
        sa.Column("alternativas", sa.JSON(), nullable=False),
        sa.Column("correta", sa.Integer(), nullable=False),
        sa.Column("explicacao", sa.Text(), nullable=False),
        sa.Column("trecho_id", sa.Integer(), sa.ForeignKey("trechos.id", ondelete="SET NULL"), nullable=True),
    )

    op.create_table(
        "respostas_simulado",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "questao_id",
            sa.Integer(),
            sa.ForeignKey("questoes.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("alternativa_escolhida", sa.Integer(), nullable=True),
        sa.Column("acertou", sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("respostas_simulado")
    op.drop_table("questoes")
    op.drop_table("simulados")
