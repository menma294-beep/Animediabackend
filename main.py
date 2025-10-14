from fastapi import FastAPI
from app.routes import user_route, post_route,comment_route, react_route, auth_route,follow_route,notification_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user_route.router)
app.include_router(post_route.router)
app.include_router(comment_route.router)
app.include_router(react_route.router)
app.include_router(auth_route.router)
app.include_router(follow_route.router)
app.include_router(notification_route.router)
print("🚀 Server started successfully!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # who can access the API (all for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
