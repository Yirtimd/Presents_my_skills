import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_API_URL = os.getenv("YANDEX_API_URL")


def request_yandex_gpt(prompt_text, max_tokens=200):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }
    payload = {
        "modelUri": "gpt://b1gveal2fp4n25u86i63/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": max_tokens
        },
        "messages": [
            {
                "role": "system",
                "text": prompt_text
            }
        ]
    }
    response = requests.post(YANDEX_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.text
    else:
        return None


def request_text(name_exist):
    name_hero = json.dumps(', '.join(person['person_name'] for person in name_exist))

    text = f'Исключи следующих супергероев, которые уже есть:{name_hero}'
    prompt = f'Сгенерируй данные существующего супергероя женщину или мужчину' \
             f'на основании данного примера и верни результат : ' \
             f'{{"gender": "Male", "id": 1, "person_name": "Superman", "power_score": 95, ' \
             f'"skills": "Flight, Super Strength, Heat Vision", {text}}}'
    result = request_yandex_gpt(prompt, max_tokens=100)
    data = json.loads(result)
    json_text = data["result"]["alternatives"][0]["message"]["text"]
    json_text = json_text.strip('`\n')
    hero_dict = json.loads(json_text)

    dumps_json = json.dumps(data)

    print(type(result))
    print(type(data))
    print(type(dumps_json))
    print(name_hero)

    return hero_dict

