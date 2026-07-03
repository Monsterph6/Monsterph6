from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.borrow import BorrowRecord, BorrowStatus
from app.models.equipment import Equipment, EquipmentStatus
from app.schemas.borrow import BorrowRecordCreate, BorrowRecordReturn


def list_borrow_records(
    db: Session,
    equipment_id: int | None = None,
    department_id: int | None = None,
    status_filter: BorrowStatus | None = None,
) -> list[BorrowRecord]:
    query = select(BorrowRecord).options(
        joinedload(BorrowRecord.equipment),
        joinedload(BorrowRecord.borrower_user),
        joinedload(BorrowRecord.borrower_department),
    )
    if equipment_id is not None:
        query = query.filter(BorrowRecord.equipment_id == equipment_id)
    if department_id is not None:
        query = query.filter(BorrowRecord.borrower_department_id == department_id)
    if status_filter is not None:
        query = query.filter(BorrowRecord.status == status_filter)
    query = query.order_by(BorrowRecord.borrow_date.desc())
    return list(db.execute(query).unique().scalars().all())


def get_overdue_borrows(db: Session) -> list[BorrowRecord]:
    """Computed on read, same pattern as maintenance alerts: no scheduler needed."""
    today = date.today()
    query = (
        select(BorrowRecord)
        .options(joinedload(BorrowRecord.equipment))
        .filter(BorrowRecord.status == BorrowStatus.borrowed)
        .filter(BorrowRecord.expected_return_date.is_not(None))
        .filter(BorrowRecord.expected_return_date < today)
        .order_by(BorrowRecord.expected_return_date.asc())
    )
    return list(db.execute(query).unique().scalars().all())


def create_borrow_record(db: Session, data: BorrowRecordCreate) -> BorrowRecord:
    equipment = db.get(Equipment, data.equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    if equipment.status != EquipmentStatus.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Thiết bị hiện không sẵn sàng để mượn (đang bảo trì/đã mượn/hỏng/ngừng sử dụng)",
        )

    record = BorrowRecord(
        code="PENDING",  # placeholder until we know the row id, replaced below
        equipment_id=data.equipment_id,
        borrower_user_id=data.borrower_user_id,
        borrower_department_id=data.borrower_department_id,
        purpose=data.purpose,
        approved_by=data.approved_by,
        borrow_date=date.today(),
        expected_return_date=data.expected_return_date,
        condition_on_borrow=data.condition_on_borrow,
        notes=data.notes,
        status=BorrowStatus.borrowed,
    )
    db.add(record)
    db.flush()  # assigns record.id without committing
    record.code = f"PM{record.id:06d}"
    equipment.status = EquipmentStatus.borrowed

    db.commit()
    db.refresh(record)
    return record


def return_borrow_record(db: Session, record: BorrowRecord, data: BorrowRecordReturn) -> BorrowRecord:
    record.actual_return_date = data.actual_return_date
    record.condition_on_return = data.condition_on_return
    record.received_by = data.received_by
    if data.notes:
        record.notes = data.notes
    record.status = BorrowStatus.returned

    equipment = db.get(Equipment, record.equipment_id)
    if equipment and equipment.status == EquipmentStatus.borrowed:
        equipment.status = EquipmentStatus.active

    db.commit()
    db.refresh(record)
    return record
