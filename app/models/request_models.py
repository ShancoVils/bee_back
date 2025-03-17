from typing import Optional

from pydantic import BaseModel


class UserParams(BaseModel):
    verified: Optional[bool] = None


class AuthParams(BaseModel):
    telegram_id: int
