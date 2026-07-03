from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.equipment import Equipment, EquipmentStatus


def list_equipment(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    department_id: int | None = None,
    status_filter: EquipmentStatus | None = None,
    category_id: int | None = None,
    search: str | None = None,
) -> tuple[list[Equipment], int]:
    query = select(Equipment)
    if department_id is not None:
        query = query.filter(Equipment.department_id == department_id)
    if status_filter is not None:
        query = query.filter(Equipment.status == status_filter)
    if category_id is not None:
        query = query.filter(Equipment.category_id == category_id)
    if search:
        like = f"%{search}%"
        query = query.filter((Equipment.name.ilike(like)) | (Equipment.code.ilike(like)))

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar_one()
    items = (
        db.execute(query.order_by(Equipment.id).offset((page - 1) * page_size).limit(page_size))
        .scalars()
        .all()
    )
    return list(items), total
