from pydantic import BaseModel, ConfigDict


class DepartmentBase(BaseModel):
    code: str
    name: str
    is_active: bool = True


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    is_active: bool | None = None


class DepartmentRead(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
