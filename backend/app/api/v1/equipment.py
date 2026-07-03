from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.equipment import Equipment, EquipmentStatus
from app.models.user import UserRole
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentListResponse,
    EquipmentRead,
    EquipmentUpdate,
)
from app.services.equipment_service import list_equipment

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("", response_model=EquipmentListResponse, dependencies=[Depends(get_current_user)])
def get_equipment_list(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    department_id: int | None = None,
    status_filter: EquipmentStatus | None = Query(None, alias="status"),
    category_id: int | None = None,
    search: str | None = None,
):
    items, total = list_equipment(db, page, page_size, department_id, status_filter, category_id, search)
    return EquipmentListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{equipment_id}", response_model=EquipmentRead, dependencies=[Depends(get_current_user)])
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    return equipment


@router.post(
    "",
    response_model=EquipmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.department_staff))],
)
def create_equipment(data: EquipmentCreate, db: Session = Depends(get_db)):
    if db.query(Equipment).filter(Equipment.code == data.code).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Equipment code already exists")
    equipment = Equipment(**data.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.put(
    "/{equipment_id}",
    response_model=EquipmentRead,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.department_staff))],
)
def update_equipment(equipment_id: int, data: EquipmentUpdate, db: Session = Depends(get_db)):
    equipment = db.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(equipment, field, value)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.delete(
    "/{equipment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(UserRole.admin))],
)
def retire_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """Soft-delete: mark retired rather than removing the row, preserving history."""
    equipment = db.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    equipment.status = EquipmentStatus.retired
    db.commit()
