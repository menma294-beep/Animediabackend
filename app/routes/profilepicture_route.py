from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.auth import get_current_user
from app.controllers.profile_picture_controller import create_profile_picture
from app.config.cloudinary_config import upload_to_cloudinary
from app.services.neo4j_service import get_driver 
router = APIRouter(prefix="/profile-picture", tags=["profile-picture"])

@router.post("/upload")
async def upload_profile_picture(file: UploadFile, current_user: dict = Depends(get_current_user)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    url = upload_to_cloudinary(file.file, folder="profile_pictures")
    result = create_profile_picture(current_user, url)
    return result

@router.get("/profile-picture/me")
def get_my_profile_picture(current_user: str = Depends(get_current_user)):
    # current_user is the user ID string
    return get_profile_picture_by_id(current_user)


# ------------------- Get any user's profile picture -------------------
@router.get("/{user_id}")
def get_profile_picture_by_id(user_id: str):
    driver = get_driver()
    query = """
    MATCH (u:User {id: $user_id})-[:HAS_PROFILE_PICTURE]->(p:ProfilePicture)
    RETURN p
    """

    try:
        with driver.session() as session:
            result = session.run(query, {"user_id": user_id}).single()

        if not result:
            # Option 1: print message to console
            print(f"⚠️ User {user_id} has no profile picture.")

            # Option 2: return a friendly JSON response
            return {
                "user_id": user_id,
                "profile_picture": None,
                "message": "User has no profile picture"
            }

        p = result["p"]
        return {
            "user_id": user_id,
            "profile_picture": {
                "id": p["id"],
                "media_url": p["media_url"],
                "created_at": str(p["created_at"])
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
