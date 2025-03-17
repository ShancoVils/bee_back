from fastapi.exceptions import HTTPException
from app.models.response_models import ExceptionsModel


class CustomExceptions(HTTPException):
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotFound(CustomExceptions):
    status_code = 404
    detail = "User not found"


class AuthenticationFailed(CustomExceptions):
    status_code = 401
    detail = "Authentication failed"
