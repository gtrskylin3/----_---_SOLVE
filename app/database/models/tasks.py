from sqlalchemy import String, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base

class Task(Base):
    """
    Модель для хранения заданий ФИПИ в базе данных.
    """
    __tablename__ = "tasks"

    # Уникальный идентификатор с сайта ФИПИ
    guid: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    # Публичный номер задания
    task_id: Mapped[str] = mapped_column(String, index=True)
    
    # Предмет (например, 'math_prof')
    subject: Mapped[str] = mapped_column(String, index=True)
    
    # Тип задания ('short_answer', 'multiple_choice', и т.д.)
    task_type: Mapped[str] = mapped_column(String)
    
    # Текстовое представление вопроса
    question_text: Mapped[str] = mapped_column(Text)
    
    # HTML-представление вопроса с MathML
    question_html: Mapped[str] = mapped_column(Text)
    
    # Единица измерения для краткого ответа (если есть)
    answer_unit: Mapped[str | None] = mapped_column(String, nullable=True)

    # Списки, хранящиеся как JSON
    images: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    kes_codes: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
