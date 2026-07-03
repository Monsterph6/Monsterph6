"""borrow workflow: add asset-borrow-slip fields, borrowed equipment status

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-10

"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE equipment_status ADD VALUE IF NOT EXISTS 'borrowed'")

    op.add_column("borrow_records", sa.Column("code", sa.String(32), nullable=True))
    op.add_column("borrow_records", sa.Column("purpose", sa.Text(), nullable=True))
    op.add_column("borrow_records", sa.Column("approved_by", sa.String(255), nullable=True))
    op.add_column("borrow_records", sa.Column("condition_on_borrow", sa.String(255), nullable=True))
    op.add_column("borrow_records", sa.Column("condition_on_return", sa.String(255), nullable=True))
    op.add_column("borrow_records", sa.Column("received_by", sa.String(255), nullable=True))

    # Backfill a code for any pre-existing rows before enforcing NOT NULL + unique.
    op.execute("UPDATE borrow_records SET code = 'PM' || LPAD(id::text, 6, '0') WHERE code IS NULL")
    op.alter_column("borrow_records", "code", nullable=False)
    op.create_index("ix_borrow_records_code", "borrow_records", ["code"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_borrow_records_code", table_name="borrow_records")
    op.drop_column("borrow_records", "received_by")
    op.drop_column("borrow_records", "condition_on_return")
    op.drop_column("borrow_records", "condition_on_borrow")
    op.drop_column("borrow_records", "approved_by")
    op.drop_column("borrow_records", "purpose")
    op.drop_column("borrow_records", "code")
    # Note: PostgreSQL cannot remove a value from an enum type; 'borrowed' stays.
