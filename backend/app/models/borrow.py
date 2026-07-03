import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class BorrowStatus(str, enum.Enum):
    borrowed = "borrowed"
    returned = "returned"
    overdue = "overdue"


class BorrowRecord(Base, TimestampMixin):
    __tablename__ = "borrow_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), index=True)
    borrower_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    borrower_department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    borrow_date: Mapped[date] = mapped_column(Date)
    expected_return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    condition_on_borrow: Mapped[str | None] = mapped_column(String(255), nullable=True)
    condition_on_return: Mapped[str | None] = mapped_column(String(255), nullable=True)
    received_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[BorrowStatus] = mapped_column(Enum(BorrowStatus, name="borrow_status"), default=BorrowStatus.borrowed)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    equipment: Mapped["Equipment"] = relationship(back_populates="borrow_records")  # noqa: F821
    borrower_user: Mapped["User | None"] = relationship()  # noqa: F821
    borrower_department: Mapped["Department | None"] = relationship()  # noqa: F821
