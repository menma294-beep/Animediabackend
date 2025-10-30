import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
def upload_to_cloudinary(file, folder="default"):
    """
    Uploads a file-like object to Cloudinary.
    Returns the public URL.
    """
    result = cloudinary.uploader.upload(file, folder=folder)
    return result["secure_url"]