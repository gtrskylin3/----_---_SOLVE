from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# URL для подключения к базе данных SQLite. 
# Файл будет создан в корневой директории проекта.
DATABASE_URL = settings.DATABASE_URL
# Создаем "движок" SQLAlchemy
engine = create_engine(
    DATABASE_URL, 
    # Этот аргумент нужен только для SQLite для корректной работы с FastAPI
    connect_args={"check_same_thread": False}
)

# Создаем класс SessionLocal, который будет фабрикой для создания сессий БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Зависимость для FastAPI, чтобы получать сессию в эндпоинтах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
