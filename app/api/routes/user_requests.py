from pyexpat import model
from typing import List, Optional, Sequence
from fastapi import APIRouter, Query, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.response_models import DistrictOut
from app.api.routes.db_methods import DataBaseMethod
from app.core.get_session import get_session
from app.models.response_models import RequestOut, RequestUpdate, RequestAdd

router = APIRouter(prefix="/requests", tags=["requests"])


@router.get("/", response_model=List[RequestOut],
            description="Получение всех заявок",
            summary="Получение пользователей")
async def get_requests(session: AsyncSession = Depends(get_session)) -> Sequence[RequestOut]:
    requests = await DataBaseMethod(session).get_requests()
    return [RequestOut.from_orm(request) for request in requests]


@router.get("/{request_id}", response_model=RequestOut,
            description="Получение заявки",
            summary="Получить заявку")
async def get_user(request_id: int, session: AsyncSession = Depends(get_session)) -> RequestOut | None:
    request = await DataBaseMethod(session, **{"request_id": request_id}).get_request_by_id()
    return RequestOut.from_orm(request)


@router.patch("/{request_id}", response_model=RequestUpdate,
              description="Верификация пользователя, меняет поле verified на true и возвращает измененный объект",
              summary="Верификация пользователя")
async def verification_user(request_id: int, request: RequestUpdate,
                            session: AsyncSession = Depends(get_session)) -> RequestUpdate | None:
    request_object = request.dict()
    request_object['request_id'] = request_id
    request = await DataBaseMethod(session, **request_object).update_request()
    return RequestUpdate.from_orm(request)


@router.post("/", response_model=RequestAdd,
             description="Регистрация пользователя",
             summary="Создание пользователя")
async def registration_user(request: RequestAdd,
                            session: AsyncSession = Depends(get_session)) -> RequestAdd | None:
    request_object = request.dict()
    request = await DataBaseMethod(session, **request_object).add_request()
    await session.close()
    return RequestAdd.from_orm(request)
