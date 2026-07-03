import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class EquipmentStatus(str, enum.Enum):
    active = "active"
    in_maintenance = "in_maintenance"
    borrowed = "borrowed"
    broken = "broken"
    retired = "retired"


class EquipmentCategory(Base, TimestampMixin):
    __tablename__ = "equipment_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    equipment: Mapped[list["Equipment"]] = relationship(back_populates="category")


class Equipment(Base, TimestampMixin):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("equipment_categories.id"), nullable=True)
    manufacturer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    serial_number: Mapped[str | None] = mapped_column(String(255), nullable=True)
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    warranty_expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True, index=True)
    status: Mapped[EquipmentStatus] = mapped_column(
        Enum(EquipmentStatus, name="equipment_status"), default=EquipmentStatus.active
    )
    specs_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    category: Mapped["EquipmentCategory"] = relationship(back_populates="equipment")
    department: Mapped["Department"] = relationship(back_populates="equipment")  # noqa: F821
    maintenance_records: Mapped[list["MaintenanceRecord"]] = relationship(back_populates="equipment")  # noqa: F821
    borrow_records: Mapped[list["BorrowRecord"]] = relationship(back_populates="equipment")  # noqa: F821
