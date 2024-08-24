from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    APP_API_URL,
    AUTH_API_URL,
)
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from loguru import logger


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "aud": APP_API_URL, "iss": AUTH_API_URL})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}


async def validate_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = token.replace("Bearer ", "")
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"decoded_jwt: {decoded_jwt}")

        expire: int = decoded_jwt.get("exp", False)
        iss = decoded_jwt.get("iss", False)
        aud = decoded_jwt.get("aud", False)

        if not iss or not aud or iss != AUTH_API_URL or aud != APP_API_URL:
            logger.info("iss or aud not valid")
            raise credentials_exception

        if not expire or expire < datetime.utcnow().timestamp():
            logger.info("email or expire not valid")
            raise credentials_exception

        return True
    except InvalidTokenError:
        raise credentials_exception
