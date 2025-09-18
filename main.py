from fastapi import FastAPI
from routes.hello_route import router as hello_router

app = FastAPI()

# include the hello route
app.include_router(hello_router)
