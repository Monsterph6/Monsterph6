from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.maintenance import MaintenanceRecord, MaintenanceRecordType, MaintenanceStatus
from app.schemas.maintenance import (
    MaintenanceRecordComplete,
    MaintenanceRecordCreate,
    MaintenanceRecordUpdate,
)


def get_upcoming_and_overdue(db: Session, window_days: int = 30) -> list[MaintenanceRecord]:
    """Computed on read: no scheduler needed for Phase 1/2.

    Rows with scheduled_date in the past are overdue; rows within window_days
    are upcoming.
    """
    today = date.today()
    query = (
        select(MaintenanceRecord)
        .options(joinedload(MaintenanceRecord.equipment))
        .filter(MaintenanceRecord.status == MaintenanceStatus.scheduled)
        .filter(MaintenanceRecord.scheduled_date <= today + timedelta(days=window_days))
        .order_by(MaintenanceRecord.scheduled_date.asc())
    )
    return list(db.execute(query).unique().scalars().all())


def list_maintenance_records(
    db: Session,
    equipment_id: int | None = None,
    status_filter: MaintenanceStatus | None = None,
    record_type: MaintenanceRecordType | None = None,
) -> list[MaintenanceRecord]:
    query = select(MaintenanceRecord).options(joinedload(MaintenanceRecord.equipment))
    if equipment_id is not None:
        query = query.filter(MaintenanceRecord.equipment_id == equipment_id)
    if status_filter is not None:
        query = query.filter(MaintenanceRecord.status == status_filter)
    if record_type is not None:
        query = query.filter(MaintenanceRecord.record_type == record_type)
    query = query.order_by(MaintenanceRecord.scheduled_date.desc())
    return list(db.execute(query).unique().scalars().all())


def create_maintenance_record(db: Session, data: MaintenanceRecordCreate) -> MaintenanceRecord:
    record = MaintenanceRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_maintenance_record(
    db: Session, record: MaintenanceRecord, data: MaintenanceRecordUpdate
) -> MaintenanceRecord:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


def complete_maintenance_record(
    db: Session, record: MaintenanceRecord, data: MaintenanceRecordComplete
) -> MaintenanceRecord:
    """Marks the record completed and, if an interval was set, schedules the next
    occurrence automatically so recurring maintenance/calibration doesn't require
    a human to remember to re-create it."""
    record.completed_date = data.completed_date
    record.performed_by = data.performed_by
    if data.notes:
        record.notes = data.notes
    record.status = MaintenanceStatus.completed

    if record.interval_days:
        next_due = data.completed_date + timedelta(days=record.interval_days)
        record.next_due_date = next_due
        db.add(
            MaintenanceRecord(
                equipment_id=record.equipment_id,
                record_type=record.record_type,
                scheduled_date=next_due,
                interval_days=record.interval_days,
                status=MaintenanceStatus.scheduled,
            )
        )

    db.commit()
    db.refresh(record)
    return record
