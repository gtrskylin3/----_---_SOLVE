import json
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine
from app.database.models import Task, Base
from app.config import settings

def load_data_from_json():
    """
    Загружает данные из JSON-файла в базу данных.
    """
    # Убедимся, что путь к файлу существует
    if not settings.PARSER_DATA_PATH.exists():
        print(f"Ошибка: Файл с данными не найден по пути {settings.PARSER_DATA_PATH}")
        return

    print("Чтение JSON-файла...")
    with open(settings.PARSER_DATA_PATH, 'r', encoding='utf-8') as f:
        tasks_data = json.load(f)

    db: Session = SessionLocal()
    
    print(f"Найдено {len(tasks_data)} задач. Начинаем загрузку в базу данных...")
    
    try:
        for index, task_dict in enumerate(tasks_data):
            # Проверяем, существует ли задача с таким guid, чтобы избежать дубликатов
            exists = db.query(Task).filter(Task.guid == task_dict["guid"]).first()
            if not exists:
                task = Task(
                    guid=task_dict["guid"],
                    task_id=task_dict["task_id"],
                    subject=task_dict["subject"],
                    task_type=task_dict["task_type"],
                    part=task_dict["part"],
                    question_text=task_dict["question_text"],
                    question_html=task_dict["question_html"],
                    answer_unit=task_dict.get("answer_unit"), # Используем .get для необязательных полей
                    images=task_dict.get("images"),
                    kes_codes=task_dict.get("kes_codes"),
                )
                db.add(task)
            
            # Периодически выводим прогресс
            if (index + 1) % 100 == 0:
                print(f"Обработано {index + 1}/{len(tasks_data)} задач...")

        print("Сохранение изменений в базе данных...")
        db.commit()
        print("[OK] Все новые задачи успешно загружены.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        db.rollback()
    finally:
        db.close()


async def create_database_tables_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # ✅ run_sync обёртка

import asyncio
if __name__ == "__main__":
    # 1. Создаем таблицы
    asyncio.run(create_database_tables_async())
    # 2. Загружаем данные
    load_data_from_json()
