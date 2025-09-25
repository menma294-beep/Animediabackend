from fastapi import APIRouter
from app.controllers.react_controller import create_react, get_reacts_for_target
from app.schemas.react_schema import ReactCreate, ReactResponse
from typing import List

router = APIRouter(prefix="/reacts")

@router.post("/", response_model=ReactResponse)
def add_react(react: ReactCreate):
    result = create_react(react.user_id, react.target_id, react.type)
    return {
        "id": result["react"]["id"],
        "type": result["react"]["type"],
        "created_at": result["react"]["created_at"],
        "user_id": result["user"]["id"],
        "username": result["user"]["username"],
        "target_id": result["target"]["id"],
        "target_type": list(result["target"].labels)[0]  # "Post" or "Comment"
    }

@router.get("/target/{target_id}", response_model=List[ReactResponse])
def list_reacts(target_id: str):
    results = get_reacts_for_target(target_id)
    return [
        {
            "id": r["react"]["id"],
            "type": r["react"]["type"],
            "created_at": r["react"]["created_at"],
            "user_id": r["user"]["id"],
            "username": r["user"]["username"],
            "target_id": r["target"]["id"],
            "target_type": list(r["target"].labels)[0]
        }
        for r in results
    ]
