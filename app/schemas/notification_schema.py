from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    receiver_id: str
    message: str
    type: str  # like, comment, follow, etc.
    target_id: Optional[str] = None
    target_type: Optional[str] = None

class NotificationResponse(BaseModel):
    id: str
    sender_id: Optional[str]
    receiver_id: Optional[str]
    sender_username: Optional[str]  # 👈 ADD THIS
    message: str
    type: str
    target_id: Optional[str] = None
    target_type: Optional[str] = None
    created_at: datetime
    is_read: bool