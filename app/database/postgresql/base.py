from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import config

engine: AsyncEngine = create_async_engine(url=config.postgresql.using_async_driver)

SessionFactory = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, class_=AsyncSession
)

Base = declarative_base()
