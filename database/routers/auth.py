from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from models import User
from db_utils.conn import get_db
from loguru import logger

router = APIRouter()


@router.post('/users/', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(user)
    return await User.create_user(db, user)

