from pydantic import BaseModel
from typing import Optional
class FollowRequest(BaseModel):
    target_user_id: str

class FollowerResponse(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
