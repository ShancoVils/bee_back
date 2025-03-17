import uuid
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, Dict, List
from app.models.base_models import UserBase, DistrictBase, RoleBase, RequestBase, RequestTypeBase
from sqlalchemy.orm import Mapped


class District(DistrictBase, table=True):
    __tablename__ = "district"

    id: int | None = Field(default=None, primary_key=True)
    district_name: str = Field(nullable=False)
    users: list["User"] = Relationship(back_populates="district")


class Role(RoleBase, table=True):
    __tablename__ = "role"

    id: int | None = Field(default=None, primary_key=True)
    role_name: str = Field(nullable=False)
    users: list["User"] = Relationship(back_populates="role")


class User(UserBase, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    fio: str = Field(nullable=False, max_length=64)
    phone_number: int = Field(nullable=False)
    organization: str = Field(nullable=False, max_length=64)
    telegram_id: int = Field(nullable=False, default=0)
    verified: Optional[bool] = Field(nullable=False)
    deleted_status: Optional[bool] = False
    deleted_comment: Optional[str] = None

    district_id: int | None = Field(default=None, nullable=False, foreign_key="district.id")
    district: Optional[District] = Relationship(back_populates="users")

    role_id: int | None = Field(default=None, nullable=False, foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="users")

    request: list["Request"] = Relationship(back_populates="user")


class RequestType(RequestTypeBase, table=True):
    __tablename__ = "request_type"

    id: int | None = Field(default=None, primary_key=True)
    request_type_name: str = Field(nullable=False, max_length=64)
    request: list["Request"] = Relationship(back_populates="request_type")


class Request(RequestBase, table=True):
    __tablename__ = "request"

    id: int | None = Field(default=None, primary_key=True)
    request_description: str = Field(nullable=False, max_length=1028)
    # photo: uuid.UUID = Field(default_factory=uuid.uuid4)
    photo:  str = Field(nullable=False, max_length=1028)
    admin_correction: str = Field(nullable=True, max_length=1028)

    user_id: int | None = Field(default=None, nullable=False, foreign_key="user.id")
    user: User | None = Relationship(back_populates="request")

    request_type_id: int | None = Field(default=None, nullable=False, foreign_key="request_type.id")
    request_type: RequestType | None = Relationship(back_populates="request")
