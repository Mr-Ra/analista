from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from config import Config
from typing import AsyncGenerator


db_engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)


async def initdb():
    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all())




async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session        
