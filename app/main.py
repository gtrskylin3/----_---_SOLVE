from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware # Added this import

from app.api.routers import tasts

app = FastAPI(title="FIPI Bank Solve Platform")

# Added CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(tasts.router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FIPI Bank Solve Platform API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
