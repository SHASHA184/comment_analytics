from fastapi import APIRouter, Depends
from security import create_access_token
from schemas.token import Token, TokenData
from security import validate_access_token
from fastapi import Header
from loguru import logger

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(token_data: TokenData):
    return create_access_token(token_data.model_dump())


@router.get("/check")
async def check(authorization=Header(default=None)):
    return await validate_access_token(authorization)