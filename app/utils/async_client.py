from typing import List
from fastapi.encoders import jsonable_encoder
from aiohttp import ClientSession
from loguru import logger
from pydantic import BaseModel
from enum import Enum

from config import DATABASE_API_URL, AUTH_API_URL


# create enum for url
class ApiUrl(Enum):
    DATABASE = DATABASE_API_URL
    AUTH = AUTH_API_URL


class DbApiAsyncClient:
    """
    Async rest client to pass info to database
    """

    @classmethod
    def get_object(cls, obj):

        if isinstance(obj, str):
            pass
        elif isinstance(obj, dict):
            pass
        elif isinstance(obj, BaseModel):
            obj = obj.dict()
        return obj

    @classmethod
    async def run_async(
        cls,
        model,
        payload=None,
        headers: dict = None,
        params: dict = None,
        path_extra: str = None,
        return_json: bool = True,
        api_url: ApiUrl = ApiUrl.DATABASE.value,
    ):
        if headers:
            req_headers = {**headers}
        else:
            req_headers = {}

        async with ClientSession() as session:
            url = api_url + "/" + model.path
            if path_extra is not None:
                url = str(url) + str(path_extra)
            payload = cls.get_object(payload)
            async with session.request(
                model.method,
                url,
                headers=req_headers,
                params=params,
                json=payload,
            ) as response:
                if response.status != 200:
                    logger.error(f"Error {response.status} with {response.text}")
                    return response
                logger.info(f"Response {response.status} with {response.text}")

                if return_json:
                    return await response.json()


class Methods:
    """Simple data structure for http methods"""

    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"


class AuthLoginRequest:
    method = Methods.POST
    path = "login/"

    @classmethod
    async def run(cls, payload):
        response = await DbApiAsyncClient.run_async(
            cls, payload, api_url=ApiUrl.AUTH.value
        )
        return response


class AuthCheckRequest:
    method = Methods.GET
    path = "check/"

    @classmethod
    async def run(cls, headers):
        response = await DbApiAsyncClient.run_async(
            cls, api_url=ApiUrl.AUTH.value, headers=headers
        )
        return response


class DbLoginRequest:
    method = Methods.POST
    path = "login/"

    @classmethod
    async def run(cls, payload):
        response = await DbApiAsyncClient.run_async(cls, payload)
        return response


class UserCreateRequest:
    method = Methods.POST
    path = "users/"

    @classmethod
    async def run(cls, payload):
        response = await DbApiAsyncClient.run_async(cls, payload)
        return response


class UserGetRequest:
    method = Methods.GET
    path = "users/"

    @classmethod
    async def run(cls, payload):
        response = await DbApiAsyncClient.run_async(cls, payload)
        return response


class PostCreateRequest:
    method = Methods.POST
    path = "posts/"

    @classmethod
    async def run(cls, payload):
        response = await DbApiAsyncClient.run_async(cls, payload)
        return response


class PostGetRequest:
    method = Methods.GET
    path = "posts/"

    @classmethod
    async def run(cls, post_id):
        response = await DbApiAsyncClient.run_async(cls, params={"post_id": post_id})
        return response


class PostListRequest:
    method = Methods.GET
    path = "posts/"

    @classmethod
    async def run(cls):
        response = await DbApiAsyncClient.run_async(cls)
        return response


class PostDeleteRequest:
    method = Methods.DELETE
    path = "posts/"

    @classmethod
    async def run(cls, post_id):
        response = await DbApiAsyncClient.run_async(cls, params={"post_id": post_id})
        return response