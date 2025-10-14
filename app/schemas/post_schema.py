from pydantic import BaseModel

class PostCreate(BaseModel):
    content: str

class PostResponse(BaseModel):
    id: str
    content: str
    created_at: str
    author_id: str
    author_username: str
