from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    """
    Базовая схема для задачи, содержащая общие поля.
    """
    guid: str
    task_id: str
    subject: str
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

