from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    post_id: int
    content: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

