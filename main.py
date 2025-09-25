from fastapi import FastAPI
from app.routes import user_route, post_route,comment_route, react_route

app = FastAPI()

app.include_router(user_route.router)
app.include_router(post_route.router)
app.include_router(comment_route.router)
app.include_router(react_route.router)