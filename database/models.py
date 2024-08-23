from sqlalchemy.orm import Session
from utils import hash_password, create_access_token, verify_password
from fastapi import HTTPException, status
from db_utils.base_model import Base
import sys
import pathlib
from datetime import timedelta

sys.path.append(str(pathlib.Path(__file__).resolve(strict=True).parent.parent))

from schemas.user import UserCreate, UserLogin
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
    async def authenticate_user(cls, db: Session, user: UserLogin):
        query = select(cls).where(cls.email == user.email)
        result = await db.execute(query)
        db_user = result.scalars().first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        
        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        # Створюємо JWT токен
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": db_user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
