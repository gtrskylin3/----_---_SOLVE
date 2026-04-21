from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import models
from app.schemas import tasks as tasks_schema
from app.database.session import get_db

router = APIRouter()

@router.get("/tasks/", response_model=List[tasks_schema.Task])
def read_tasks(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 100, 
    kes_code: Optional[str] = None
):
    """
    Получить список задач с возможностью пагинации и фильтрации по коду КЭС.
    """
    query = db.query(models.Task)
    
    # Фильтруем по коду КЭС, если он предоставлен
    if kes_code:
        # Ищем задачи, у которых в JSON-списке kes_codes содержится нужная строка
        query = query.filter(models.Task.kes_codes.contains(kes_code))
        
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=tasks_schema.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Получить одну задачу по ее ID.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

