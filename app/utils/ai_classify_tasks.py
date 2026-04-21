from app.config import settings, ai_settings
import json
import time
import re
from tqdm import tqdm
from openai import OpenAI


BASE_DIR = settings.BASE_DIR
PARSER_DATA_PATH = settings.PARSER_DATA_PATH

FILE = PARSER_DATA_PATH
PROMPT_FILE = BASE_DIR / "utils" / "system-prompt.md"

SYSTEM_PROMPT = open(PROMPT_FILE, encoding="utf-8").read()


# ===== GitHub Models =====
endpoint = "https://models.github.ai/inference"

token = ai_settings.API_KEY  # ⚠️ тут у тебя должен быть GitHub token
model_name = ai_settings.MODEL_NAME  # например: "openai/gpt-4o-mini"


client = OpenAI(
    base_url=endpoint,
    api_key=token,
)


def llm_call(user_prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                max_tokens=200,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            sleep_time = 2 ** attempt
            print(f"LLM error retry {attempt+1}/{max_retries}: {e}")
            time.sleep(sleep_time)

    return ""


def classify_task(task):
    text = task.get("question_text", "")
    kes = task.get("kes_codes", [])

    user_prompt = f"""
    Текст задачи:
    {text}

    KES:
    {kes}
    """

    result = llm_call(user_prompt)

    nums = re.findall(r"\d+", result)
    return int(nums[0]) if nums else None


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, task in enumerate(tqdm(data)):
        if "ege_number" in task:
            continue

        try:
            task["ege_number"] = classify_task(task)

            # не пишем файл после каждого запроса (важно)
            if i % 10 == 0:
                save(data)

            time.sleep(1.2)  # rate limit protection

        except Exception as e:
            print("Ошибка:", e)

    save(data)
    print("Готово")


if __name__ == "__main__":
    main()


