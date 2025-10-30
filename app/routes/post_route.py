from fastapi import APIRouter, Depends, HTTPException
from app.controllers import post_controller
from app.auth import get_current_user
from fastapi import UploadFile, File, Form
from app.controllers.post_controller import create_media_post
from app.schemas.post_schema import PostCreate, PostResponse
from app.controllers.post_controller import create_post, get_all_posts,get_posts_by_user
router = APIRouter(prefix="/posts", tags=["posts"])




@router.post("/", response_model=PostResponse)
def add_post(post: PostCreate, current_user: str = Depends(get_current_user)):
    result = create_post(post.content, current_user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": result["post"]["id"],
        "content": result["post"]["content"],
        "created_at": result["post"]["created_at"],
        "author_id": result["user"]["id"],
        "author_username": result["user"]["username"]
    }




@router.get("/")
def list_posts(current_user: dict = Depends(get_current_user)):
    return post_controller.get_all_posts()

@router.get("/user/{user_id}")
def list_user_posts(user_id: str, current_user: dict = Depends(get_current_user)):
    posts = post_controller.get_posts_by_user(user_id)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")
    return posts

@router.post("/media", response_model=PostResponse)
def add_media_post(
    file: UploadFile = File(...),
    content: str = Form(None),
    current_user: dict = Depends(get_current_user)
):
    try:
        result = create_media_post(current_user, file, content)
        return {
            "id": result["post"]["id"],
            "content": result["post"]["content"],
            "media_url": result["post"]["media_url"],
            "media_type": result["post"]["media_type"],
            "created_at": result["post"]["created_at"],
            "author_id": result["user"]["id"],
            "author_username": result["user"]["username"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


