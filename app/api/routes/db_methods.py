from typing import Any, Sequence

from sqlmodel import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from app.models.db_models import User, Role, District, Request, RequestType
from app.models.response_models import UserOut, UserUpdate, UserRegistration, RequestUpdate, RequestAdd


class DataBaseMethod:
    def __init__(self, session: AsyncSession, **kwargs: Any) -> None:
        self.session = session
        self.kwargs = kwargs

    async def fetch_users(self) -> Sequence[User]:
        verified = self.kwargs.get('verified', None)
        query = select(User).options(selectinload(User.district), selectinload(User.role))
        if verified is not None:
            # Добавляем условие на фильтрацию, если verified True или False
            query = query.where(User.verified == verified)
        result = await self.session.scalars(query)
        return result.all()

    async def fetch_user(self) -> User | None:
        user_id = self.kwargs.get('user_id', None)
        query = select(User).options(selectinload(User.district), selectinload(User.role)).filter(User.id == user_id)
        result = await self.session.scalars(query)
        return result.first()

    async def update_user(self) -> User | None:
        user_id = self.kwargs.get('user_id', None)

        query = select(User).filter(User.id == user_id).options(selectinload(User.district),
                                                                selectinload(User.role))
        result = await self.session.scalars(query)
        user = result.first()
        update_data = UserUpdate.from_orm(self.kwargs)

        if update_data.fio is not None:
            user.fio = update_data.fio
        if update_data.phone_number is not None:
            user.phone_number = update_data.phone_number
        if update_data.organization is not None:
            user.organization = update_data.organization
        if update_data.telegram_id is not None:
            user.telegram_id = update_data.telegram_id
        if update_data.verified is not None:
            user.verified = update_data.verified

        # Проверяем и обновляем идентификатор района, если он присутствует
        if update_data.district and update_data.district.id is not None:
            user.district_id = update_data.district.id

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def add(self) -> User | None:

        new_user = UserUpdate.from_orm(self.kwargs)

        role_query = select(Role).filter_by(role_name="user")
        role = await self.session.scalars(role_query)
        role = role.first()
        district_query = select(District).filter_by(id=new_user.district.id)
        district = await self.session.scalars(district_query)
        district = district.first()

        new_user_add = User(
            fio=new_user.fio,
            role=role,
            district=district,
            verified=True,
            phone_number=new_user.phone_number,
            telegram_id=None,
            organization=new_user.organization,
        )
        self.session.add(new_user_add)
        await self.session.commit()

        query = select(User).filter(User.id == new_user_add.id).options(selectinload(User.district))
        result = await self.session.scalars(query)
        user = result.first()
        return user

    async def delete(self) -> User | None:
        user_id = self.kwargs.get('user_id', None)

        query = select(User).filter(User.id == user_id).options(selectinload(User.district))
        result = await self.session.scalars(query)
        user = result.first()

        update_data = UserUpdate.from_orm(self.kwargs)

        if update_data.deleted_comment is not None:
            user.deleted_comment = update_data.deleted_comment
        user.deleted_status = True

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def auth(self) -> User | None:
        telegram_id = self.kwargs.get('telegram_id', None)

        query = select(User).filter(User.telegram_id == telegram_id).options(selectinload(User.district))
        result = await self.session.scalars(query)
        user = result.first()
        return user

    async def get_districts(self) -> Sequence[District]:
        query = select(District)
        result = await self.session.scalars(query)
        return result.all()

    async def get_requests(self) -> Sequence[Request]:
        query = (
            select(Request)
            .options(
                selectinload(Request.request_type),
                selectinload(Request.user)
                .selectinload(User.district)

            )
        )
        result = await self.session.scalars(query)
        return result.all()

    async def get_request_by_id(self) -> Sequence[Request]:
        request_id = self.kwargs.get('request_id', None)
        query = (
            select(Request)
            .options(
                selectinload(Request.request_type),
                selectinload(Request.user)
                .selectinload(User.district)

            )
        ).filter(Request.id == request_id)
        result = await self.session.scalars(query)
        return result.first()

    async def update_request(self) -> User | None:
        request_id = self.kwargs.get('request_id', None)

        query = select(Request).options(selectinload(Request.request_type)).filter(Request.id == request_id)
        result = await self.session.scalars(query)

        request = result.first()
        update_data = RequestUpdate.from_orm(self.kwargs)

        if update_data.admin_correction is not None:
            request.admin_correction = update_data.admin_correction

        # Проверяем и обновляем идентификатор района, если он присутствует
        if update_data.request_type and update_data.request_type.id is not None:
            request.request_type_id = update_data.request_type.id

        await self.session.commit()
        await self.session.refresh(request)
        return request

    async def add_request(self) -> Request | None:
        new_request = RequestAdd.from_orm(self.kwargs)
        request_type_query = select(RequestType).filter_by(id=new_request.request_type.id)
        request_type = await self.session.scalars(request_type_query)
        request_type = request_type.first()

        new_request_add = Request(
            request_description=new_request.request_description,
            request_type=request_type,
            admin_correction=None,
            photo=new_request.photo,
            user_id=new_request.user_id
        )
        self.session.add(new_request_add)
        await self.session.commit()

        query = select(Request).filter(Request.id == new_request_add.id).options(selectinload(Request.request_type))
        result = await self.session.scalars(query)
        return result.first()
