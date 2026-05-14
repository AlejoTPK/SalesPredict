"""Initial schema: users and sales tables

Revision ID: 001_initial
Revises:
Create Date: 2025-05-14 00:00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(320), unique=True, index=True, nullable=False),
        sa.Column("hashed_password", sa.Text, nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_superuser", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "sales",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("product_id", sa.String(100), index=True, nullable=False),
        sa.Column("product_name", sa.String(500), nullable=False),
        sa.Column("customer_id", sa.String(36), index=True, nullable=True),
        sa.Column("customer_name", sa.String(500), nullable=True),
        sa.Column("region", sa.String(255), index=True, nullable=True),
        sa.Column("status", sa.String(50), default="completed"),
        sa.Column("sale_date", sa.DateTime(timezone=True), index=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("sales")
    op.drop_table("users")
