import uuid
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, Dict, List


class UserBase(SQLModel):
    id: int
    fio: str
    phone_number: int
    organization: str
    telegram_id: int
    verified: bool
    deleted_status: bool
    deleted_comment: Optional[str]


class DistrictBase(SQLModel):
    id: int
    district_name: str


class RoleBase(SQLModel):
    id: int
    role_name: str


class RequestTypeBase(SQLModel):
    id: int
    request_type_name: str


class RequestBase(SQLModel):
    id: int
    request_description: str
    photo: str
    admin_correction: str = Field(nullable=False, max_length=1028)
