from pyexpat import model
from typing import List, Optional, Sequence
from fastapi import APIRouter, Query, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.response_models import DistrictOut
from app.api.routes.db_methods import DataBaseMethod
from app.core.get_session import get_session

router = APIRouter(prefix="/districts", tags=["districts"])


@router.get("/", response_model=List[DistrictOut],
            description="Получение списка муниципалитетов",
            summary="Получение муниципалитетов")
async def get_users(session: AsyncSession = Depends(get_session)) -> Sequence[DistrictOut]:
    districts = await DataBaseMethod(session).get_districts()
    return [DistrictOut.from_orm(district) for district in districts]
