from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON
from typing import List

from app.database.models.base import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    nickname: Mapped[str] = mapped_column(unique=True, index=True)
    solved_tasks: Mapped[List[int]] = mapped_column(JSON, default=[], nullable=False)
