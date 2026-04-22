import json
from app.config import settings

FILE = settings.PARSER_DATA_PATH

with open(str(FILE).replace('.json', 'short_version.json'), "w", encoding="utf-8") as out_file:
    with open(FILE, "r", encoding="utf-8") as in_file:
        data = json.load(in_file)
        short_data = []
        for i, task in enumerate(data):
            text = task.get("question_text", "")
            kes = task.get("kes_codes", [])
            task_id = task.get("task_id", [])
            images = task.get("images", None)
            
            is_images = False

            if images and all('.png' in i for i in images):
                is_images = True
            # Сохраняем выбранные данные в словарь
            short_data.append({
                "task_id": task_id,
                "question_text": text,
                "kes_codes": kes,
                "is_images": is_images
            })
        
        # Записываем выбранные данные в файл
        json.dump(short_data, out_file, ensure_ascii=False, indent=4)