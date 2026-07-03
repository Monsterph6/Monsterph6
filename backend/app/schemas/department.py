from pydantic import BaseModel, ConfigDict, field_validator

from app.core.text_utils import normalize_code


class DepartmentBase(BaseModel):
    code: str
    name: str
    is_active: bool = True

    @field_validator("code")
    @classmethod
    def _normalize_code(cls, v: str) -> str:
        return normalize_code(v)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    is_active: bool | None = None

    @field_validator("code")
    @classmethod
    def _normalize_code(cls, v: str | None) -> str | None:
        return normalize_code(v) if v is not None else v


class DepartmentRead(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
