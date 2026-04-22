from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func # Added func
from typing import List
from collections import defaultdict

from app.auth import current_required_user
from app.database import models
from app.database.models.users import User
from app.database.models.tasks import Task # Added Task
from app.database.session import get_async_session
from app.schemas import tasks as tasks_schema
from app.schemas.users import DashboardStats, MarkTaskDoneRequest

router = APIRouter()

@router.post("/tasks/{task_id}/mark_done")
async def mark_task_done(
    task_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_required_user),
):
    """
    Отметить задачу как выполненную для авторизованного пользователя.
    """
    db_task = await db.get(models.Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_id not in user.solved_tasks:
        user.solved_tasks = user.solved_tasks + [task_id]
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    return {"message": f"Task {task_id} marked as done for user {user.nickname}"}


@router.get("/me/dashboard-stats", response_model=DashboardStats)
async def get_dashboard_stats(
    user: User = Depends(current_required_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Получить статистику решенных задач для текущего пользователя.
    """
    solved_task_ids = user.solved_tasks
    total_solved = len(solved_task_ids)

    # Calculate total number of tasks
    total_tasks_stmt = select(func.count(Task.id))
    total_tasks = (await db.execute(total_tasks_stmt)).scalar_one()

    if not solved_task_ids:
        return DashboardStats(total_solved=0, solved_by_kes={}, total_tasks=total_tasks)

    # Fetch solved tasks to get their KES codes
    stmt = select(models.Task).filter(models.Task.id.in_(solved_task_ids))
    result = await db.execute(stmt)
    solved_tasks = result.scalars().all()

    solved_by_kes = defaultdict(int)
    for task in solved_tasks:
        if task.kes_codes:
            for kes_code in task.kes_codes:
                # Use only the main part of the KES code (e.g., "1.1")
                main_kes_part = kes_code.split(' ')[0]
                solved_by_kes[main_kes_part] += 1
        
    return DashboardStats(
        total_solved=total_solved, 
        solved_by_kes=solved_by_kes, 
        total_tasks=total_tasks
    )


@router.get("/me/solved-tasks", response_model=List[tasks_schema.Task])
async def get_solved_tasks(
    user: User = Depends(current_required_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Получить список всех решенных задач текущего пользователя.
    """
    solved_task_ids = user.solved_tasks
    if not solved_task_ids:
        return []

    stmt = select(models.Task).filter(models.Task.id.in_(solved_task_ids))
    result = await db.execute(stmt)
    solved_tasks = result.scalars().all()

    return solved_tasks
