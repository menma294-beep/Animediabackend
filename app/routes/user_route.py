from fastapi import APIRouter
from app.controllers.user_controller import create_user, get_all_users,create_friendship,get_user_friends
from app.schemas.user_schema import UserCreate, UserResponse
from typing import List
from app.schemas.user_schema import FriendshipRequest
router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate):
    new_user = create_user(user.username, user.email)
    return {
        "id": new_user["id"],
        "username": new_user["username"],
        "email": new_user["email"]
    }
@router.get("/", response_model=List[UserResponse])
def list_users():
    users = get_all_users()
    return [{"id": u["id"], "username": u["username"], "email": u["email"]} for u in users]

@router.post("/friends")
def add_friendship(request: FriendshipRequest):
    result = create_friendship(request.user_id, request.friend_id)
    if not result:
        return {"error": "Users not found"}
    return {
        "user": result["user"]["username"],
        "friend": result["friend"]["username"]
    }
    
@router.get("/{user_id}/friends", response_model=List[UserResponse])
def list_friends(user_id: str):
    friends = get_user_friends(user_id)
    return [{"id": f["id"], "username": f["username"], "email": f["email"]} for f in friends]
