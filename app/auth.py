from fastapi import Depends, HTTPException, status
import jwt
import os
from app.config.settings import JWT_SECRET
from fastapi.security import HTTPBearer

oauth2_scheme = HTTPBearer()
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

def get_current_user(credentials = Depends(security)):
    token = credentials.credentials  # Extract the token
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
