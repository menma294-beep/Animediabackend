from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.auth import get_current_user
from app.controllers.profile_picture_controller import create_profile_picture
from app.config.cloudinary_config import upload_to_cloudinary

router = APIRouter(prefix="/profile-picture", tags=["profile-picture"])

@router.post("/upload")
async def upload_profile_picture(file: UploadFile, current_user: dict = Depends(get_current_user)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    url = upload_to_cloudinary(file.file, folder="profile_pictures")
    result = create_profile_picture(current_user, url)
    return result
