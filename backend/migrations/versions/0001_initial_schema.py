"""initial schema: departments, users, equipment, maintenance, borrow

Revision ID: 0001
Revises:
Create Date: 2026-07-03

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

user_role = sa.Enum("admin", "department_staff", "technician", name="user_role")
equipment_status = sa.Enum("active", "in_maintenance", "broken", "retired", name="equipment_status")
maintenance_record_type = sa.Enum("maintenance", "calibration", name="maintenance_record_type")
maintenance_status = sa.Enum("scheduled", "completed", "overdue", "cancelled", name="maintenance_status")
borrow_status = sa.Enum("borrowed", "returned", "overdue", name="borrow_status")


def upgrade() -> None:
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    equipment_status.create(bind, checkfirst=True)
    maintenance_record_type.create(bind, checkfirst=True)
    maintenance_status.create(bind, checkfirst=True)
    borrow_status.create(bind, checkfirst=True)

    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(32), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_departments_code", "departments", ["code"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(64), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="department_staff"),
        sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id"), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "equipment_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "equipment",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("equipment_categories.id"), nullable=True),
        sa.Column("manufacturer", sa.String(255), nullable=True),
        sa.Column("model", sa.String(255), nullable=True),
        sa.Column("serial_number", sa.String(255), nullable=True),
        sa.Column("purchase_date", sa.Date(), nullable=True),
        sa.Column("warranty_expiry_date", sa.Date(), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id"), nullable=True),
        sa.Column("status", equipment_status, nullable=False, server_default="active"),
        sa.Column("specs_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_equipment_code", "equipment", ["code"], unique=True)
    op.create_index("ix_equipment_department_id", "equipment", ["department_id"])

    op.create_table(
        "maintenance_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("equipment_id", sa.Integer(), sa.ForeignKey("equipment.id"), nullable=False),
        sa.Column("record_type", maintenance_record_type, nullable=False),
        sa.Column("scheduled_date", sa.Date(), nullable=False),
        sa.Column("completed_date", sa.Date(), nullable=True),
        sa.Column("status", maintenance_status, nullable=False, server_default="scheduled"),
        sa.Column("performed_by", sa.String(255), nullable=True),
        sa.Column("next_due_date", sa.Date(), nullable=True),
        sa.Column("interval_days", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_maintenance_records_equipment_id", "maintenance_records", ["equipment_id"])
    op.create_index("ix_maintenance_records_scheduled_date", "maintenance_records", ["scheduled_date"])

    op.create_table(
        "borrow_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("equipment_id", sa.Integer(), sa.ForeignKey("equipment.id"), nullable=False),
        sa.Column("borrower_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("borrower_department_id", sa.Integer(), sa.ForeignKey("departments.id"), nullable=True),
        sa.Column("borrow_date", sa.Date(), nullable=False),
        sa.Column("expected_return_date", sa.Date(), nullable=True),
        sa.Column("actual_return_date", sa.Date(), nullable=True),
        sa.Column("status", borrow_status, nullable=False, server_default="borrowed"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_borrow_records_equipment_id", "borrow_records", ["equipment_id"])


def downgrade() -> None:
    op.drop_table("borrow_records")
    op.drop_table("maintenance_records")
    op.drop_table("equipment")
    op.drop_table("equipment_categories")
    op.drop_table("users")
    op.drop_table("departments")

    bind = op.get_bind()
    borrow_status.drop(bind, checkfirst=True)
    maintenance_status.drop(bind, checkfirst=True)
    maintenance_record_type.drop(bind, checkfirst=True)
    equipment_status.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
