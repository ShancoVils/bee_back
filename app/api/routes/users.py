from pyexpat import model
from typing import List, Optional, Sequence
from fastapi import APIRouter, Query, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.response_models import UserOut, UserUpdate, UserRegistration, DeleteComment
from app.api.routes.db_methods import DataBaseMethod
from app.models.request_models import UserParams
from app.core.get_session import get_session
from app.utils.exeptions import UserNotFound

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut],
            description="Получение всех пользователей, с/без указания статуса верификации",
            summary="Получение пользователей")
async def get_users(params: UserParams = Query(), session: AsyncSession = Depends(get_session)) -> Sequence[UserOut]:
    users = await DataBaseMethod(session, **params.dict()).fetch_users()
    user_outs = [UserOut.from_orm(user) for user in users]
    return user_outs


@router.get("/{user_id}", response_model=UserOut,
            description="Получение пользователя по идентификатору",
            summary="Получение пользователя")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> UserOut | None:
    user = await DataBaseMethod(session, **{"user_id": user_id}).fetch_user()
    if user is None:
        raise UserNotFound
    return UserOut.from_orm(user)


@router.patch("/{user_id}", response_model=UserUpdate,
              description="Верификация пользователя, меняет поле verified на true и возвращает измененный объект",
              summary="Верификация пользователя")
async def verification_user(user_id: int, user: UserUpdate,
                            session: AsyncSession = Depends(get_session)) -> UserUpdate | None:
    user_object = user.dict()
    user_object['user_id'] = user_id
    user = await DataBaseMethod(session, **user_object).update_user()
    if user is None:
        raise UserNotFound
    return UserUpdate.from_orm(user)


@router.post("/", response_model=UserRegistration,
             description="Регистрация пользователя",
             summary="Создание пользователя")
async def registration_user(user: UserRegistration,
                            session: AsyncSession = Depends(get_session)) -> UserRegistration | None:
    user_object = user.dict()
    user = await DataBaseMethod(session, **user_object).add()
    await session.close()
    return UserRegistration.from_orm(user)


@router.patch("/{user_id}", response_model=UserOut,
               description="Удаление пользователя с пояснением",
               summary="Удаление пользователя")
async def delete_user(user_id: int, delete_comment: DeleteComment,
                      session: AsyncSession = Depends(get_session)) -> UserOut | None:
    user_object = delete_comment.dict()
    user_object['user_id'] = user_id
    user = await DataBaseMethod(session, **user_object).delete()
    return UserOut.from_orm(user)
