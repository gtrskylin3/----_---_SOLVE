
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    BASE_DIR: Path = BASE_DIR
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/fipi_tasks.db"
    PARSER_DATA_PATH: Path = BASE_DIR / "parser" / "data"/ "math_tasks.json"

# class AISettings(BaseSettings):
#     model_config = SettingsConfigDict(env_file=BASE_DIR/".env", extra="ignore")
#     MODEL_NAME: str 
#     API_KEY: str 

# Создаем экземпляр настроек, который можно будет импортировать
settings = Settings()
# ai_settings = AISettings()