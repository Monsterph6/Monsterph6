from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.text_utils import normalize_code
from app.models.equipment import EquipmentStatus


class EquipmentCategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class EquipmentBase(BaseModel):
    code: str
    name: str
    category_id: int | None = None
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    purchase_date: date | None = None
    warranty_expiry_date: date | None = None
    location: str | None = None
    department_id: int | None = None
    status: EquipmentStatus = EquipmentStatus.active
    specs_notes: str | None = None

    @field_validator("code")
    @classmethod
    def _normalize_code(cls, v: str) -> str:
        return normalize_code(v)


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    purchase_date: date | None = None
    warranty_expiry_date: date | None = None
    location: str | None = None
    department_id: int | None = None
    status: EquipmentStatus | None = None
    specs_notes: str | None = None


class EquipmentRead(EquipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EquipmentListResponse(BaseModel):
    items: list[EquipmentRead]
    total: int
    page: int
    page_size: int
