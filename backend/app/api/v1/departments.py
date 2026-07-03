from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.department import Department
from app.models.user import UserRole
from app.schemas.department import DepartmentCreate, DepartmentRead, DepartmentUpdate

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("", response_model=list[DepartmentRead], dependencies=[Depends(get_current_user)])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).order_by(Department.name).all()


@router.post(
    "",
    response_model=DepartmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.admin))],
)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    if db.query(Department).filter(Department.code == data.code).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Department code already exists")
    department = Department(**data.model_dump())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.put(
    "/{department_id}",
    response_model=DepartmentRead,
    dependencies=[Depends(require_role(UserRole.admin))],
)
def update_department(department_id: int, data: DepartmentUpdate, db: Session = Depends(get_db)):
    department = db.get(Department, department_id)
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(department, field, value)
    db.commit()
    db.refresh(department)
    return department
