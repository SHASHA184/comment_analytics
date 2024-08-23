from fastapi import APIRouter
from schemas.user import UserCreate, UserResponse, UserLogin
from config import DATABASE_API_URL
import aiohttp

router = APIRouter()

@router.post('/users/')
async def create_user(user: UserCreate):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{DATABASE_API_URL}/users/", json=user.model_dump()) as response:
            response_data = await response.json()
            if response.status != 200:
                return response_data
            return UserResponse(**response_data)

@router.post("/login")
async def login(user: UserLogin):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{DATABASE_API_URL}/login/", json=user.model_dump()) as response:
            response_data = await response.json()
            if response.status != 200:
                return response_data
            return response_data