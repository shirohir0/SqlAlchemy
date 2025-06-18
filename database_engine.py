from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, insert
from config import settings
import asyncio

class Base(DeclarativeBase):
    pass

sync_engine = create_engine(
    url = settings.DATABASE_URL_psycopg,
    echo = False,
)

async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = False,
)
make_sync_session = sessionmaker(bind = sync_engine)
make_async_session = async_sessionmaker(bind = async_engine)