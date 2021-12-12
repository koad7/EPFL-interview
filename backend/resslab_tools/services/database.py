"""
Database Service
"""
from typing import AsyncIterator
from urllib.parse import quote_plus

from alembic.command import upgrade
from alembic.config import Config
from resslab_tools.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__username = settings.postgres_user  # type: ignore
__password = settings.postgres_password  # type: ignore
__database = settings.postgres_db  # type: ignore
__host = settings.database_host  # type: ignore
__port = settings.database_port  # type: ignore
__credential = f'{__username}:{quote_plus(__password)}'
__url_without_driver = f'://{__credential}@{__host}:{__port}/{__database}'
url = 'postgresql' + __url_without_driver
async_url = 'postgresql+asyncpg' + __url_without_driver

engine = create_async_engine(async_url, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession)

Base = declarative_base(bind=engine)


def upgrade_database():
    """
    Run database migration with alembic
    https://alembic.sqlalchemy.org/en/latest/api/commands.html
    """
    alembic_cfg = Config('alembic.ini')
    upgrade(alembic_cfg, 'head')


async def get_session() -> AsyncIterator[AsyncSession]:
    """
    Get session for FastAPI routers
    https://github.com/uriyyo/fastapi-pagination/blob/main/examples/pagination_async_sqlalchemy.py
    """
    async with async_session() as session:
        yield session
