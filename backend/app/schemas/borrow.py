from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.borrow import BorrowStatus


class BorrowRecordCreate(BaseModel):
    equipment_id: int
    borrower_user_id: int | None = None
    borrower_department_id: int | None = None
    purpose: str | None = None
    approved_by: str | None = None
    expected_return_date: date | None = None
    condition_on_borrow: str | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def _require_a_borrower(self):
        if self.borrower_user_id is None and self.borrower_department_id is None:
            raise ValueError("Phải chọn người mượn hoặc phòng ban mượn")
        return self


class BorrowRecordReturn(BaseModel):
    actual_return_date: date = Field(default_factory=date.today)
    condition_on_return: str | None = None
    received_by: str | None = None
    notes: str | None = None


class BorrowRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    equipment_id: int
    equipment_code: str | None = None
    equipment_name: str | None = None
    borrower_user_id: int | None
    borrower_user_name: str | None = None
    borrower_department_id: int | None
    borrower_department_name: str | None = None
    purpose: str | None
    approved_by: str | None
    borrow_date: date
    expected_return_date: date | None
    actual_return_date: date | None
    condition_on_borrow: str | None
    condition_on_return: str | None
    received_by: str | None
    status: BorrowStatus
    notes: str | None
