from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.maintenance import MaintenanceRecordType, MaintenanceStatus


class MaintenanceRecordBase(BaseModel):
    equipment_id: int
    record_type: MaintenanceRecordType
    scheduled_date: date
    interval_days: int | None = None
    notes: str | None = None


class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass


class MaintenanceRecordUpdate(BaseModel):
    scheduled_date: date | None = None
    interval_days: int | None = None
    notes: str | None = None


class MaintenanceRecordComplete(BaseModel):
    completed_date: date = Field(default_factory=date.today)
    performed_by: str | None = None
    notes: str | None = None


class MaintenanceRecordRead(MaintenanceRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed_date: date | None
    status: MaintenanceStatus
    performed_by: str | None
    next_due_date: date | None
    equipment_code: str | None = None
    equipment_name: str | None = None
