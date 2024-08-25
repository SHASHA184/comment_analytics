from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db_utils.conn import get_db
from schemas.post import PostCreate, PostResponse
from models import Post
from loguru import logger

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    new_post = await Post.create_post(db, post)
    return new_post

@router.get("/", response_model=list[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    posts = await Post.get_posts(db)
    logger.info(posts)
    return posts

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(post_id)
    post = await Post.get_post(db, post_id)
    logger.info(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/{post_id}", response_model=PostResponse)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await Post.delete_post(db, post_id)
    return post
