from pydantic import BaseModel
from typing import Optional

class ReactCreate(BaseModel):
    target_id: str
    react_type: str

class ReactResponse(BaseModel):
    id: Optional[str]
    type: Optional[str] = None
    created_at: Optional[str] = None
    user_id: Optional[str] = None
    user_username: Optional[str] = None
    target_id: Optional[str] = None
    is_active: Optional[bool] = True
