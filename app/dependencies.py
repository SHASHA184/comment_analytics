from utils.async_client import AuthCheckRequest
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger


async def get_oauth2_scheme(request: Request):
    try:
        oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        oauth2_scheme = await oauth2_scheme.__call__(request)
    except HTTPException as ex:
        oauth2_scheme = ex
    return oauth2_scheme

async def check_user(request: Request, token = Depends(get_oauth2_scheme)):
    if isinstance(token, HTTPException):
        raise token
    return await AuthCheckRequest.run(headers={"Authorization": "Bearer " + token})