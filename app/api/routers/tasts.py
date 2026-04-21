from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import models
from app.schemas import tasks as tasks_schema
from app.database.session import get_db
from app.parser.src.checker import FIPIChecker
from app.parser.src.models import Task as ParserTask, TaskType

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

@router.post("/tasks/{task_id}/check", response_model=tasks_schema.AnswerCheckResponse)
def check_task_answer(
    task_id: int,
    answer_request: tasks_schema.AnswerCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Проверить ответ на задачу.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    checker = FIPIChecker(subject_key='math_prof')
    
    # Создаем временный объект Task, который ожидает checker
    parser_task = ParserTask(
        guid=db_task.guid,
        task_id=db_task.task_id,
        subject=db_task.subject,
        task_type=TaskType(db_task.task_type),
        question_text=db_task.question_text,
        question_html=db_task.question_html
    )

    check_result = checker.check_answer(parser_task, answer_request.answer)

    return tasks_schema.AnswerCheckResponse(
        guid=check_result.guid,
        result=check_result.result.value,
        user_answer=check_result.user_answer
    )
