from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

class FriendshipRequest(BaseModel):
    user_id: str
    friend_id: str
