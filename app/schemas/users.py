import uuid
from fastapi_users import schemas
from typing import List, Dict

class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: str
    solved_tasks: List[int]

class UserCreate(schemas.BaseUserCreate):
    nickname: str

class UserUpdate(schemas.BaseUserUpdate):
    nickname: str

class DashboardStats(schemas.BaseModel):
    total_solved: int
    solved_by_kes: Dict[str, int]
    total_tasks: int

class MarkTaskDoneRequest(schemas.BaseModel):
    task_id: int
