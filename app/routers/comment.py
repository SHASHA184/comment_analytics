from fastapi import APIRouter
from schemas.comment import CommentCreate, CommentResponse
from typing import List
from dependencies import check_user
from fastapi import Depends
from utils.async_client import (
    CommentCreateRequest,
    CommentGetRequest,
    CommentListRequest,
    CommentDeleteRequest,
    CommentListRangeRequest
)
from loguru import logger
from datetime import date

router = APIRouter(
    dependencies=[Depends(check_user)], tags=["comment"], prefix="/comments"
)


@router.post("/", response_model=CommentResponse)
async def create_comment(comment: CommentCreate):
    db_response = await CommentCreateRequest.run(comment)
    return db_response


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int):
    db_response = await CommentGetRequest.run(comment_id)
    return db_response


@router.get("/", response_model=List[CommentResponse])
async def get_comments():
    db_response = await CommentListRequest.run()
    return db_response


@router.delete("/{comment_id}", response_model=CommentResponse)
async def delete_comment(comment_id: int):
    db_response = await CommentDeleteRequest.run(comment_id)
    return db_response


@router.get("/comments-daily-breakdown/", response_model=List[CommentResponse])
async def get_comments_daily_breakdown(date_from: date, date_to: date):
    date_from_str = date_from.strftime('%Y-%m-%d')
    date_to_str = date_to.strftime('%Y-%m-%d')
    db_response = await CommentListRangeRequest.run(date_from_str, date_to_str)
    return db_response