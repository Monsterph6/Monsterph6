from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.maintenance import MaintenanceRecord, MaintenanceRecordType, MaintenanceStatus
from app.models.user import UserRole
from app.schemas.maintenance import (
    MaintenanceRecordComplete,
    MaintenanceRecordCreate,
    MaintenanceRecordRead,
    MaintenanceRecordUpdate,
)
from app.services.maintenance_service import (
    complete_maintenance_record,
    create_maintenance_record,
    get_upcoming_and_overdue,
    list_maintenance_records,
    update_maintenance_record,
)

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

_can_manage = require_role(UserRole.admin, UserRole.technician)


def _to_read(record: MaintenanceRecord) -> MaintenanceRecordRead:
    data = MaintenanceRecordRead.model_validate(record)
    data.equipment_code = record.equipment.code
    data.equipment_name = record.equipment.name
    return data


@router.get("/alerts", response_model=list[MaintenanceRecordRead], dependencies=[Depends(get_current_user)])
def get_alerts(db: Session = Depends(get_db), window_days: int = 30):
    records = get_upcoming_and_overdue(db, window_days)
    return [_to_read(r) for r in records]


@router.get("", response_model=list[MaintenanceRecordRead], dependencies=[Depends(get_current_user)])
def get_maintenance_records(
    db: Session = Depends(get_db),
    equipment_id: int | None = None,
    status_filter: MaintenanceStatus | None = None,
    record_type: MaintenanceRecordType | None = None,
):
    records = list_maintenance_records(db, equipment_id, status_filter, record_type)
    return [_to_read(r) for r in records]


@router.post(
    "",
    response_model=MaintenanceRecordRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(_can_manage)],
)
def create_record(data: MaintenanceRecordCreate, db: Session = Depends(get_db)):
    record = create_maintenance_record(db, data)
    return _to_read(record)


@router.put(
    "/{record_id}",
    response_model=MaintenanceRecordRead,
    dependencies=[Depends(_can_manage)],
)
def update_record(record_id: int, data: MaintenanceRecordUpdate, db: Session = Depends(get_db)):
    record = db.get(MaintenanceRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance record not found")
    record = update_maintenance_record(db, record, data)
    return _to_read(record)


@router.post(
    "/{record_id}/complete",
    response_model=MaintenanceRecordRead,
    dependencies=[Depends(_can_manage)],
)
def complete_record(record_id: int, data: MaintenanceRecordComplete, db: Session = Depends(get_db)):
    record = db.get(MaintenanceRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance record not found")
    if record.status != MaintenanceStatus.scheduled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only scheduled records can be completed")
    record = complete_maintenance_record(db, record, data)
    return _to_read(record)
