from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    content: Optional[str] = None  # optional since media-only posts are allowed

class PostResponse(BaseModel):
    id: str
    content: Optional[str] = None
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    created_at: str
    author_id: str
    author_username: str

