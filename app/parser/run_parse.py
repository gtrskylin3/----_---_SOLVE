import os
import sys

# Добавляем корень проекта в sys.path для корректных импортов
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.parser.src.parser import FIPIParser

def main():
    """
    Основная функция для запуска парсера ФИПИ.
    """
    # Инициализация парсера для профильной математики
    math_parser = FIPIParser('math_prof')

    # Полноценный запуск для всех заданий
    math_parser.parse_all_tasks(output_file="app/parser/data/math_tasks.json")

if __name__ == "__main__":
    main()

