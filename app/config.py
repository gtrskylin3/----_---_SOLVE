
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Определяем базовую директорию проекта (она же директория 'app')
    BASE_DIR: Path = Path(__file__).resolve().parent

    # URL базы данных SQLite. Файл будет находиться в директории 'app'.
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/fipi_tasks.db"

    # Путь к JSON-файлу с данными парсера (предполагаем, что он в app/parser/math_tasks.json)
    PARSER_DATA_PATH: Path = BASE_DIR / "parser" / "data"/ "math_tasks.json"

    # Конфигурация Pydantic-settings
    # Позволяет загружать переменные из .env файла
    # 'extra="ignore"' игнорирует неизвестные переменные в .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Создаем экземпляр настроек, который можно будет импортировать
settings = Settings()