from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

# Создаем асинхронный движок
engine = create_async_engine("sqlite+aiosqlite:///beedatabase.db", echo=False)

# Создаем сессию с помощью sessionmaker
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
