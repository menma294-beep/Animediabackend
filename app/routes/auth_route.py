from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import SignupRequest, LoginRequest, TokenResponse
from app.controllers.auth_controller import signup_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=TokenResponse)
def signup(payload: SignupRequest):
    token = signup_user(payload.username, payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=400, detail="Signup failed")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    token = login_user(payload.username, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
