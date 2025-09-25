from fastapi import APIRouter
from app.controllers.post_controller import create_post, get_all_posts
from app.schemas.post_schema import PostCreate, PostResponse
from typing import List

router = APIRouter(prefix="/posts")

@router.post("/", response_model=PostResponse)
def add_post(post: PostCreate):
    result = create_post(post.user_id, post.content)
    return {
        "id": result["post"]["id"],
        "content": result["post"]["content"],
        "created_at": result["post"]["created_at"],
        "author_id": result["user"]["id"],
        "author_username": result["user"]["username"]
    }

@router.get("/", response_model=List[PostResponse])
def list_posts():
    results = get_all_posts()
    return [
        {
            "id": r["post"]["id"],
            "content": r["post"]["content"],
            "created_at": r["post"]["created_at"],
            "author_id": r["user"]["id"],
            "author_username": r["user"]["username"]
        }
        for r in results
    ]
from app.controllers.post_controller import get_posts_by_user

@router.get("/user/{user_id}", response_model=List[PostResponse])
def list_user_posts(user_id: str):
    results = get_posts_by_user(user_id)
    return [
        {
            "id": r["post"]["id"],
            "content": r["post"]["content"],
            "created_at": r["post"]["created_at"],
            "author_id": r["user"]["id"],
            "author_username": r["user"]["username"]
        }
        for r in results
    ]
