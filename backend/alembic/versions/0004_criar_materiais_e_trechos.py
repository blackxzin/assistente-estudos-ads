"""cria materiais e trechos

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-27

"""
from collections.abc import Sequence

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

from alembic import op
from app.config import configuracoes

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

tipo_material = sa.Enum("pdf", "texto", name="tipo_material", create_type=False)
status_material = sa.Enum("processando", "pronto", "erro", name="status_material", create_type=False)


def upgrade() -> None:
    tipo_material.create(op.get_bind(), checkfirst=True)
    status_material.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "materiais",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "disciplina_id",
            sa.Integer(),
            sa.ForeignKey("disciplinas.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("tipo", tipo_material, nullable=False),
        sa.Column("status", status_material, nullable=False, server_default="processando"),
        sa.Column("resumo", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "trechos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "material_id",
            sa.Integer(),
            sa.ForeignKey("materiais.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("conteudo", sa.Text(), nullable=False),
        sa.Column("pagina", sa.Integer(), nullable=True),
        sa.Column("posicao", sa.Integer(), nullable=False),
        sa.Column("embedding", Vector(configuracoes.EMBEDDING_DIM), nullable=False),
    )

    op.execute("CREATE INDEX ix_trechos_embedding_hnsw ON trechos USING hnsw (embedding vector_cosine_ops)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_trechos_embedding_hnsw")
    op.drop_table("trechos")
    op.drop_table("materiais")
    status_material.drop(op.get_bind(), checkfirst=True)
    tipo_material.drop(op.get_bind(), checkfirst=True)
