from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db_utils.conn import get_db
from schemas.comment import CommentCreate, CommentResponse
from models import Comment
from loguru import logger
from typing import List
from datetime import date

router = APIRouter(tags=["comment"], prefix="/comments")

@router.post("/", response_model=CommentResponse)
async def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    new_comment = await Comment.create_comment(db, comment)
    return new_comment

@router.get("/", response_model=List[CommentResponse])
async def get_comments(db: AsyncSession = Depends(get_db)):
    comments = await Comment.get_comments(db)
    return comments

@router.get("/comments-daily-breakdown/", response_model=List[CommentResponse])
async def get_comments_daily_breakdown(date_from: str, date_to: str, db: AsyncSession = Depends(get_db)):
    comments = await Comment.get_comments_daily_breakdown(db, date_from, date_to)
    return comments

@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await Comment.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment

@router.delete("/{comment_id}", response_model=CommentResponse)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await Comment.delete_comment(db, comment_id)
    return comment