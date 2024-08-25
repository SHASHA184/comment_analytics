from fastapi import APIRouter
from schemas.user import UserCreate, UserResponse, UserLogin
from config import DATABASE_API_URL
import aiohttp
from utils.async_client import DbLoginRequest, AuthLoginRequest, UserCreateRequest

router = APIRouter(tags=["auth"])


@router.post("/users/")
async def create_user(user: UserCreate):
    db_response = await UserCreateRequest.run(user)
    return db_response


@router.post("/login")
async def login(user: UserLogin):
    db_response = await DbLoginRequest.run(user)
    if db_response is False:
        return db_response
    auth_response = await AuthLoginRequest.run(user)
    return auth_response
