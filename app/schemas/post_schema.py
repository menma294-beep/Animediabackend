from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    user_id: str
    content: str

class PostResponse(BaseModel):
    id: str
    content: str
    created_at: datetime
    author_id: str
    author_username: str
