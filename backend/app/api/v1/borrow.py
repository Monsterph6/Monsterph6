from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.borrow import BorrowRecord, BorrowStatus
from app.models.user import UserRole
from app.schemas.borrow import BorrowRecordCreate, BorrowRecordRead, BorrowRecordReturn
from app.services.borrow_service import (
    create_borrow_record,
    get_overdue_borrows,
    list_borrow_records,
    return_borrow_record,
)

router = APIRouter(prefix="/borrow", tags=["borrow"])

_can_manage = require_role(UserRole.admin, UserRole.department_staff)


def _to_read(record: BorrowRecord) -> BorrowRecordRead:
    data = BorrowRecordRead.model_validate(record)
    data.equipment_code = record.equipment.code
    data.equipment_name = record.equipment.name
    data.borrower_user_name = record.borrower_user.full_name if record.borrower_user else None
    data.borrower_department_name = record.borrower_department.name if record.borrower_department else None
    return data


@router.get("/overdue", response_model=list[BorrowRecordRead], dependencies=[Depends(get_current_user)])
def get_overdue(db: Session = Depends(get_db)):
    return [_to_read(r) for r in get_overdue_borrows(db)]


@router.get("", response_model=list[BorrowRecordRead], dependencies=[Depends(get_current_user)])
def get_borrow_records(
    db: Session = Depends(get_db),
    equipment_id: int | None = None,
    department_id: int | None = None,
    status_filter: BorrowStatus | None = None,
):
    records = list_borrow_records(db, equipment_id, department_id, status_filter)
    return [_to_read(r) for r in records]


@router.post(
    "",
    response_model=BorrowRecordRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(_can_manage)],
)
def create_record(data: BorrowRecordCreate, db: Session = Depends(get_db)):
    record = create_borrow_record(db, data)
    return _to_read(record)


@router.post(
    "/{record_id}/return",
    response_model=BorrowRecordRead,
    dependencies=[Depends(_can_manage)],
)
def return_record(record_id: int, data: BorrowRecordReturn, db: Session = Depends(get_db)):
    record = db.get(BorrowRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")
    if record.status != BorrowStatus.borrowed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only borrowed records can be returned")
    record = return_borrow_record(db, record, data)
    return _to_read(record)
