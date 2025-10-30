from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.controllers.bio_controller import create_or_update_bio
from pydantic import BaseModel

router = APIRouter(prefix="/bio", tags=["bio"])

class BioUpdate(BaseModel):
    birthday: str | None = None
    status: str | None = None
    about: str | None = None
    hobbies: str | None = None
    skills: str | None = None
    interest_tags: str | None = None
    school: str | None = None

@router.post("/update")
def update_bio(bio: BioUpdate, current_user: dict = Depends(get_current_user)):
    result = create_or_update_bio(
        current_user,
        bio.birthday,
        bio.status,
        bio.about,
        bio.hobbies,
        bio.skills,
        bio.interest_tags,
        bio.school
    )
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.get("/me")
def get_my_bio(current_user: dict = Depends(get_current_user)):
    query = """
    MATCH (u:User {id: $user_id})-[:HAS_BIO]->(b:Bio)
    RETURN b
    """
    from app.services.neo4j_service import run_query
    result = run_query(query, {"user_id": current_user}, single=True)
    if not result:
        raise HTTPException(status_code=404, detail="No bio found")
    return result["b"]

@router.get("/{user_id}")
def get_user_bio(user_id: str, current_user: dict = Depends(get_current_user)):
    query = """
    MATCH (u:User {id: $user_id})-[:HAS_BIO]->(b:Bio)
    RETURN b
    """
    from app.services.neo4j_service import run_query
    result = run_query(query, {"user_id": user_id}, single=True)
    if not result:
        raise HTTPException(status_code=404, detail="This user has no bio")
    return result["b"]
