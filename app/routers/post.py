from fastapi import APIRouter
from schemas.post import PostCreate, PostResponse
from typing import List
from dependencies import check_user
from fastapi import Depends
from utils.async_client import (
    PostCreateRequest,
    PostGetRequest,
    PostListRequest,
    PostDeleteRequest,
)
from utils.moderate_text import moderate_text
from loguru import logger

router = APIRouter(dependencies=[Depends(check_user)], tags=["post"], prefix="/posts")


@router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate):
    db_response = await PostCreateRequest.run(post)
    return db_response


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    db_response = await PostGetRequest.run(post_id)
    return db_response


@router.get("/", response_model=List[PostResponse])
async def get_posts():
    db_response = await PostListRequest.run()
    return db_response


@router.delete("/{post_id}", response_model=PostResponse)
async def delete_post(post_id: int):
    db_response = await PostDeleteRequest.run(post_id)
    return db_response

@router.get("/moderate/{post_id}", response_model=PostResponse)
async def moderate_post(post_id: int):
    moderation_response = await moderate_text("I hate you!")
    db_response = await PostGetRequest.run(post_id)
    post = PostResponse(**db_response)
    logger.info(post)
    moderation_response = await moderate_text(post.content)
    logger.info(moderation_response)
    return db_response