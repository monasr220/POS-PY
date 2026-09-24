import os
from typing import AsyncGenerator

from dotenv import  load_dotenv
from sqlalchemy.ext.asyncio import(
    AsyncSession ,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL enviroment varlibale is not set")
for prefix in ("postgresql://","postgresql://"):
    if DATABASE_URL.startswith(prefix):
        DATABASE_URL = DATABASE_URL.replace(prefix,"postgresql+asyncnpg://",1)
        break
    
DATABASE_URL = DATABASE_URL.replace("sslmode=" ,"sll")

engine = create_async_engine(
    DATABASE_URL,
    echo = os.getenv("SQL_ECHO","false").lower() == "true",
    pool_pre_ping = True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db()-> AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
        yield session