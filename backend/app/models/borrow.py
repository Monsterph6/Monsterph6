import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class BorrowStatus(str, enum.Enum):
    borrowed = "borrowed"
    returned = "returned"
    overdue = "overdue"


class BorrowRecord(Base, TimestampMixin):
    """Schema ships in Phase 1; borrow/return workflow and UI land in Phase 3."""

    __tablename__ = "borrow_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), index=True)
    borrower_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    borrower_department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    borrow_date: Mapped[date] = mapped_column(Date)
    expected_return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[BorrowStatus] = mapped_column(Enum(BorrowStatus, name="borrow_status"), default=BorrowStatus.borrowed)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    equipment: Mapped["Equipment"] = relationship(back_populates="borrow_records")  # noqa: F821
