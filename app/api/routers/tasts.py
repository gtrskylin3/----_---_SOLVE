from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
import asyncio

from app.database import models
from app.schemas import tasks as tasks_schema
from app.database.session import get_async_session
from app.parser.src.checker import FIPIChecker
from app.parser.src.models import Task as ParserTask, TaskType

from app.auth import current_active_user
from app.database.models.users import User

router = APIRouter()

@router.get("/tasks/", response_model=tasks_schema.TaskListResponse)
async def read_tasks(
    db: AsyncSession = Depends(get_async_session),
    user: Optional[User] = Depends(current_active_user),
    skip: int = 0,
    limit: int = 15, # Changed default to 15
    kes_code: Optional[str] = None,
    task_type_filter: Optional[str] = None,
    part_filter: Optional[int] = None,
):
    """
    Получить список задач с возможностью пагинации и фильтрации.
    Для авторизованных пользователей исключает уже решенные задачи.
    """
    query = select(models.Task)

    if kes_code:
        query = query.where(models.Task.kes_codes.contains(kes_code))

    if task_type_filter:
        if task_type_filter == 'short-answer':
            query = query.where(models.Task.task_type == 'short_answer')
        elif task_type_filter == 'not-short-answer':
            query = query.where(models.Task.task_type != 'short_answer')
    
    if part_filter:
        query = query.where(models.Task.part == part_filter)
    
    if user and user.solved_tasks:
        query = query.where(models.Task.id.notin_(user.solved_tasks))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Get paginated tasks
    tasks_query = query.offset(skip).limit(limit)
    tasks_result = await db.execute(tasks_query)
    tasks = tasks_result.scalars().all()

    return tasks_schema.TaskListResponse(tasks=tasks, total=total)

@router.get("/tasks/{task_id}", response_model=tasks_schema.Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    """
    Получить одну задачу по ее ID.
    """
    db_task = await db.get(models.Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.post("/tasks/{task_id}/check", response_model=tasks_schema.AnswerCheckResponse)
async def check_task_answer(
    task_id: int,
    answer_request: tasks_schema.AnswerCheckRequest,
    db: AsyncSession = Depends(get_async_session),
    user: Optional[User] = Depends(current_active_user),
):
    """
    Проверить ответ на задачу. Если пользователь авторизован и ответ верный,
    задача добавляется в список решенных.
    """
    db_task = await db.get(models.Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    checker = FIPIChecker(subject_key='math_prof')
    
    parser_task = ParserTask(
        guid=db_task.guid, task_id=db_task.task_id, subject=db_task.subject,
        part=db_task.part,task_type=TaskType(db_task.task_type), question_text=db_task.question_text,
        question_html=db_task.question_html
    )

    # Run synchronous checker in a thread pool
    loop = asyncio.get_event_loop()
    check_result = await loop.run_in_executor(
        None, checker.check_answer, parser_task, answer_request.answer
    )

    solved_tasks_list = None
    if user and check_result.result.value == "correct":
        if task_id not in user.solved_tasks:
            # SQLAlchemy JSON modification requires creating a new list
            user.solved_tasks = user.solved_tasks + [task_id]
            db.add(user)
            await db.commit()
            await db.refresh(user)
        solved_tasks_list = user.solved_tasks
    elif user:
        solved_tasks_list = user.solved_tasks


    return tasks_schema.AnswerCheckResponse(
        guid=check_result.guid,
        result=check_result.result.value,
        user_answer=check_result.user_answer,
        solved_tasks=solved_tasks_list
    )
