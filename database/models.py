from sqlalchemy.orm import Session
from utils import hash_password, verify_password
from fastapi import HTTPException, status
from db_utils.base_model import Base
import sys
import pathlib
from datetime import timedelta
from sqlalchemy.sql import func

sys.path.append(str(pathlib.Path(__file__).resolve(strict=True).parent.parent))

from schemas.user import UserCreate, UserLogin
from schemas.post import PostCreate
from schemas.comment import CommentCreate
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
from datetime import date

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
    async def get_user(cls, db: Session, email: str):
        query = select(cls).where(cls.email == email)
        result = await db.execute(query)
        return True if result.scalars().first() else False

    @classmethod
    async def authenticate_user(cls, db: Session, user: UserLogin):
        query = select(cls).where(cls.email == user.email)
        result = await db.execute(query)
        db_user = result.scalars().first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return True if db_user else False


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    @classmethod
    async def create_post(cls, db: Session, post: PostCreate):
        new_post = cls(**post.model_dump())
        await new_post.save(db)
        return new_post

    @classmethod
    async def get_post(cls, db: Session, post_id: int):
        query = select(cls).where(cls.id == post_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_posts(cls, db: Session, skip: int = 0, limit: int = 10):
        query = select(cls).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def delete_post(cls, db: Session, post_id: int):
        query = select(cls).where(cls.id == post_id)
        result = await db.execute(query)
        post = result.scalars().first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        await post.delete(db)
        return post


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    @classmethod
    async def create_comment(cls, db: Session, comment: CommentCreate):
        new_comment = cls(**comment.model_dump())
        await new_comment.save(db)
        return new_comment

    @classmethod
    async def get_comment(cls, db: Session, comment_id: int):
        query = select(cls).where(cls.id == comment_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_comments(cls, db: Session, skip: int = 0, limit: int = 10):
        query = select(cls).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_comments_daily_breakdown(
        cls, db: Session, date_from: str, date_to: str
    ):
        date_from = date.fromisoformat(date_from)
        date_to = date.fromisoformat(date_to)
        query = (
            select(cls)
            .where(cls.created_at >= date_from)
            .where(cls.created_at <= date_to)
        )
        result = await db.execute(query)
        return result.scalars().all()   

    @classmethod
    async def delete_comment(cls, db: Session, comment_id: int):
        query = select(cls).where(cls.id == comment_id)
        result = await db.execute(query)
        comment = result.scalars().first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
            )
        await comment.delete(db)
        return comment
