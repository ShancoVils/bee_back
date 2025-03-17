from pydantic import BaseModel

from app.models.base_models import DistrictBase, RoleBase, UserBase, RequestBase, RequestTypeBase
from typing import Optional


class DistrictOut(DistrictBase):
    id: int


class RoleOut(RoleBase):
    id: int


class UserUpdate(UserBase):
    id: Optional[int] = None
    fio: Optional[str] = None
    organization: Optional[str] = None
    phone_number: Optional[int] = None
    verified: Optional[bool] = None
    telegram_id: Optional[int] = None

    district: Optional[DistrictOut] = None
    deleted_status: bool = False
    deleted_comment: Optional[str] = None


class UserRegistration(UserBase):
    id: Optional[int] = None
    fio: str
    organization: str
    phone_number: int
    verified: bool = True
    telegram_id: Optional[int] = None
    district: DistrictOut
    deleted_status: bool = False
    deleted_comment: Optional[str] = None


class UserOut(UserBase):
    id: int
    district: Optional[DistrictOut] = None


class RequestOut(RequestBase):
    request_type: Optional[RequestTypeBase] = None
    admin_correction: Optional[str] = None
    user: Optional[UserOut] = None


class RequestUpdate(RequestBase):
    id: Optional[int] = None
    request_description: Optional[str] = None
    photo: Optional[str] = None
    admin_correction: Optional[str] = None
    request_type: Optional[RequestTypeBase] = None


class RequestAdd(RequestBase):
    id: Optional[int] = None
    request_description: str
    photo: Optional[str] = None
    admin_correction: Optional[str] = None
    request_type: Optional[RequestTypeBase] = None
    user_id: int


class DeleteComment(BaseModel):
    deleted_comment: str


class ExceptionsModel(BaseModel):
    detail: str
