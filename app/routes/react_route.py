from fastapi import APIRouter, Depends
from app.schemas.react_schema import ReactCreate, ReactResponse
from app.controllers.react_controller import create_react, get_reactors_for_post, set_react_inactive
from app.auth import get_current_user

router = APIRouter(prefix="/reacts", tags=["Reacts"])

@router.post("/", response_model=ReactResponse)
def add_react(
    react: ReactCreate,
    current_user: str = Depends(get_current_user)
):
    return create_react(user_id=current_user, target_id=react.target_id, react_type=react.react_type)


@router.post("/unlike", response_model=ReactResponse)
def unlike_react(
    react: ReactCreate,
    current_user: str = Depends(get_current_user)
):
    return set_react_inactive(user_id=current_user, target_id=react.target_id)


@router.get("/post/{post_id}")
def list_post_reacts(
    post_id: str,
    current_user: str = Depends(get_current_user)
):
    return get_reactors_for_post(post_id, current_user)
