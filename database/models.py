from sqlalchemy.orm import Session
from utils import hash_password
from fastapi import HTTPException, status
from db_utils.base_model import Base
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve(strict=True).parent.parent))

from schemas.user import UserCreate
from sqlalchemy.sql.expression import select
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Enum,
    DECIMAL,
    ForeignKey,
    select,
    JSON,
    Text,
    Boolean,
)

from loguru import logger


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    @classmethod
    async def create_user(cls, db: Session, user: UserCreate):
        # Перевірка, чи існує користувач
        query = select(cls).where(cls.email == user.email)
        result = await db.execute(query)
        instance = result.scalars().first()
        logger.info(instance)
        if instance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered",
            )

        # Створення нового користувача
        new_user = cls(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
        )

        await new_user.save(db)

        return new_user

    @classmethod
    def get_user(cls, db: Session, user_id: int):
        return db.query(cls).filter(cls.id == user_id).first()
