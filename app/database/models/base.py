from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer

class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    Автоматически добавляет первичный ключ 'id'.
    """
    __abstract__ = True # Указывает, что это не таблица, а базовый класс

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
