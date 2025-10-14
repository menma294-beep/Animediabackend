from fastapi import APIRouter, Depends
from typing import List
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.controllers.comment_controller import create_comment, get_comments_for_post
from app.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse)
def add_comment(
    comment: CommentCreate,
    current_user: str = Depends(get_current_user)  # 👈 logged-in user
):
    result = create_comment(current_user, comment.post_id, comment.content)
    return {
        "id": result["comment"]["id"],
        "content": result["comment"]["content"],
        "created_at": result["comment"]["created_at"],
        "author_id": result["user"]["id"],
        "author_username": result["user"]["username"],
        "post_id": result["post"]["id"]
    }

@router.get("/post/{post_id}", response_model=List[CommentResponse])
def list_comments(
    post_id: str,
    current_user: str = Depends(get_current_user)  # 👈 must be logged in
):
    results = get_comments_for_post(post_id)
    return [
        {
            "id": r["comment"]["id"],
            "content": r["comment"]["content"],
            "created_at": r["comment"]["created_at"],
            "author_id": r["user"]["id"],
            "author_username": r["user"]["username"],
            "post_id": r["post"]["id"]
        }
        for r in results
    ]
