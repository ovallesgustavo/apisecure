from fastapi import FastAPI
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.auth import router as auth_router

app = FastAPI()

app.include_router(users_router, prefix="/api/v1/user")
app.include_router(auth_router, prefix="/api/v1/auth")

@app.get("/")
def read_root():
    return {"message": "Welcome to Apisecure!"}
