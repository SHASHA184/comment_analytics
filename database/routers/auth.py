from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse, UserLogin
from models import User
from db_utils.conn import get_db
from loguru import logger

router = APIRouter(tags=["auth"])


@router.post('/users/', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(user)
    return await User.create_user(db, user)

@router.get('/users/')
async def get_user(email: str, db: Session = Depends(get_db)) -> bool:
    return await User.get_user(db, email)

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_user = await User.authenticate_user(db, user)
    return auth_user