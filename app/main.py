from fastapi import FastAPI
import uvicorn

from app.api.routers import tasts

app = FastAPI(title="FIPI Bank Solve Platform")

app.include_router(tasts.router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FIPI Bank Solve Platform API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
