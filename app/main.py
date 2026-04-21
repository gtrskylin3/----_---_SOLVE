from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import uuid

from app.api.routers import tasts, kes, user_data
from app.database.models.users import User
from app.database.session import create_db_and_tables
from app.schemas.users import UserRead, UserCreate, UserUpdate
from app.auth import auth_backend, fastapi_users

app = FastAPI(title="FIPI Bank Solve Platform")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Adjust for your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generic exception handler to see error details
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print(f"An unhandled exception occurred: {repr(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected server error occurred.", "detail": repr(exc)},
    )

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

app.include_router(tasts.router, prefix="/api/v1", tags=["tasks"])
app.include_router(kes.router, prefix="/api/v1", tags=["kes"])
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/cookie", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(user_data.router, prefix="/api/v1", tags=["user_data"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FIPI Bank Solve Platform API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True)
