from fastapi import APIRouter
from controllers.hello_controller import get_hello

router = APIRouter()

@router.get("/")
def read_root():
    return get_hello()
