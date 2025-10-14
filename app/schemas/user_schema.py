from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    last_active: Optional[datetime] = None  # 👈 new field

class FriendshipRequest(BaseModel):
    user_id: str
    friend_id: str
