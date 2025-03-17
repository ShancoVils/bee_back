from pyexpat import model
from typing import List, Optional, Sequence
from fastapi import APIRouter, Query, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.response_models import UserOut, ExceptionsModel
from app.api.routes.db_methods import DataBaseMethod
from app.core.get_session import get_session
from app.models.request_models import AuthParams
from app.utils.exeptions import AuthenticationFailed

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/user", response_model=UserOut,
            description="Авторизация",
            summary="Авторизация")
async def get_users(params: AuthParams = Query(), session: AsyncSession = Depends(get_session)) -> UserOut:
    user = await DataBaseMethod(session, **params.dict()).auth()
    if user is None:
        raise AuthenticationFailed
    return UserOut.from_orm(user)
