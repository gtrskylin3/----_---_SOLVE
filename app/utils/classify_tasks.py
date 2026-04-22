import json
import os

def get_part(task):
    text = task.get("question_text", "").lower()
    
    # ===== ЧАСТЬ 2 (развёрнутый ответ) =====
    
    # Экономические задачи (кредиты, вклады)
    if any(word in text for word in ["кредит", "вклад", "платёж", "банк", "млн рублей", "долг", "процентная ставка"]):
        return 2
    
    # Параметр
    if "параметр" in text or "все значения a" in text:
        return 2
    
    # Неравенство
    if "решите неравенство" in text:
        return 2
    
    # Уравнение с отбором корней
    if "решите уравнение" in text and ("найдите все корни" in text or "принадлежащие отрезку" in text):
        return 2
    
    # Геометрия с доказательством
    if "докажите" in text:
        return 2
    
    # Пункты "а)" и "б)"
    if "а)" in text and "б)" in text:
        return 2
    
    # ===== ВСЁ ОСТАЛЬНОЕ — ЧАСТЬ 1 =====
    return 1


# def main():
#     script_dir = os.path.dirname(__file__)
#     parser_data_path = os.path.join(script_dir, '..', 'parser', 'data', 'math_tasksshort_version.json')
#     output_path = os.path.join(script_dir, 'tasks_with_part.json')
    
#     try:
#         with open(parser_data_path, 'r', encoding='utf-8') as f:
#             tasks = json.load(f)
#     except FileNotFoundError:
#         print(f"Ошибка: файл не найден {parser_data_path}")
#         return
    
#     results = []
#     stats = {1: 0, 2: 0}
    
#     for task in tasks:
#         part = get_part(task)
#         results.append({
#             "task_id": task["task_id"],
#             "text_preview": task['question_text'][:80],
#             "kes_codes": task.get('kes_codes', []),
#             "part": part
#         })
#         stats[part] += 1
    
#     with open(output_path, 'w', encoding='utf-8') as f:
#         json.dump(results, f, ensure_ascii=False, indent=4)
    
#     print("=" * 40)
#     print("СТАТИСТИКА")
#     print("=" * 40)
#     print(f"Часть 1: {stats[1]} задач")
#     print(f"Часть 2: {stats[2]} задач")
#     print(f"\nРезультаты сохранены в {output_path}")


# if __name__ == "__main__":
#     main()