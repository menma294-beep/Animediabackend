from pydantic import BaseModel
from datetime import datetime

class ReactCreate(BaseModel):
    user_id: str
    target_id: str   # could be a Post or Comment
    type: str        # e.g., "like", "love", "haha"

class ReactResponse(BaseModel):
    id: str
    type: str
    created_at: datetime
    user_id: str
    username: str
    target_id: str
    target_type: str
