from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    """
    Базовая схема для задачи, содержащая общие поля.
    """
    guid: str
    task_id: str
    subject: str
    part: int
    task_type: str
    question_text: str
    question_html: str
    answer_unit: Optional[str] = None
    images: Optional[List[str]] = []
    kes_codes: Optional[List[str]] = []

class Task(TaskBase):
    """
    Основная схема для отображения задачи, включая ID из базы данных.
    """
    id: int

    # Конфигурация для работы с моделями SQLAlchemy (ORM)
    class Config:
        from_attributes = True

class AnswerCheckRequest(BaseModel):
    """
    Схема для запроса на проверку ответа.
    """
    answer: str

class AnswerCheckResponse(BaseModel):
    """
    Схема для ответа с результатом проверки.
    """
    guid: str
    result: str # "correct", "incorrect", "error"
    user_answer: str
    solved_tasks: Optional[List[int]] = None

class TaskListResponse(BaseModel):
    """
    Схема для ответа со списком задач и общим количеством.
    """
    tasks: List[Task]
    total: int
