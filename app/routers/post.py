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
from loguru import logger

router = APIRouter(dependencies=[Depends(check_user)])


@router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate):
    db_response = await PostCreateRequest.run(post)
    return db_response


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    logger.info(f"Getting post with id: {post_id}")
    db_response = await PostGetRequest.run(post_id)
    return db_response


@router.get("/", response_model=List[PostResponse])
async def get_posts():
    logger.info("Getting all posts")
    db_response = await PostListRequest.run()
    return db_response


@router.delete("/{post_id}", response_model=PostResponse)
async def delete_post(post_id: int):
    db_response = await PostDeleteRequest.run(post_id)
    return db_response
