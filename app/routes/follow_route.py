from fastapi import APIRouter, Depends
from typing import List
from app.schemas.follow_schema import FollowRequest, FollowerResponse
from app.controllers.follow_controller import follow_user, get_followers
from app.auth import get_current_user

router = APIRouter(prefix="/follows", tags=["Follows"])

@router.post("/", response_model=FollowerResponse)
def add_follow(
    follow_req: FollowRequest,
    current_user: str = Depends(get_current_user)
):
    result = follow_user(current_user, follow_req.target_user_id)
    return {
        "id": result["followee"]["id"],
        "username": result["followee"]["username"],
        "email": result["followee"].get("email")  # ✅ safer
    }

@router.get("/followers/{user_id}", response_model=List[FollowerResponse])
def list_followers(
    user_id: str,
    current_user: str = Depends(get_current_user)
):
    results = get_followers(user_id)
    return [
        {
            "id": r["id"],
            "username": r["username"],
            "email": r.get("email")  # ✅ safer
        }
        for r in results
    ]
