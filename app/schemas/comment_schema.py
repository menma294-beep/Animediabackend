from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    user_id: str
    post_id: str
    content: str

class CommentResponse(BaseModel):
    id: str
    content: str
    created_at: datetime
    author_id: str
    author_username: str
    post_id: str
