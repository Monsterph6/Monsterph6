import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class MaintenanceRecordType(str, enum.Enum):
    maintenance = "maintenance"
    calibration = "calibration"


class MaintenanceStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    overdue = "overdue"
    cancelled = "cancelled"


class MaintenanceRecord(Base, TimestampMixin):
    """Schema ships in Phase 1; scheduling/alert business logic and UI land in Phase 2."""

    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), index=True)
    record_type: Mapped[MaintenanceRecordType] = mapped_column(
        Enum(MaintenanceRecordType, name="maintenance_record_type")
    )
    scheduled_date: Mapped[date] = mapped_column(Date, index=True)
    completed_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[MaintenanceStatus] = mapped_column(
        Enum(MaintenanceStatus, name="maintenance_status"), default=MaintenanceStatus.scheduled
    )
    performed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    interval_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    equipment: Mapped["Equipment"] = relationship(back_populates="maintenance_records")  # noqa: F821
