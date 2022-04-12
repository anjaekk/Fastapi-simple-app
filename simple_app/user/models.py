import asyncio
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from core.database import Base
from sqlmodel import Field, SQLModel


class User(Base): #true:db에서 사용할 테이블 확인(false시 테이블 생성안됨)
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    name = Column(String(20), nullable=True)
    is_active = Column(Boolean, unique=False, default=True, nullable=False)
    created = Column(DateTime, server_default=func.utc_timstamp())
    jwt_token_key = Column(String(200), nullable=True)