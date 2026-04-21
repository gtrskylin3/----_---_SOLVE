from src.parser import FIPIParser

def main():
    """
    Основная функция для запуска парсера ФИПИ.
    """
    # Инициализация парсера для профильной математики
    math_parser = FIPIParser('math_prof')

    # Запуск парсинга всех заданий.
    # Для тестового запуска можно ограничить количество заданий, например:
    # math_parser.parse_all_tasks(max_tasks=50, output_file="math_tasks_test.json")
    
    # Полноценный запуск для всех заданий
    math_parser.parse_all_tasks(output_file="app/parser/data/math_tasks.json")

if __name__ == "__main__":
    main()
