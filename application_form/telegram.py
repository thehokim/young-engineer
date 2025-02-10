import requests

# Замените токен на новый, если предыдущий уже использовался в открытом виде!
TELEGRAM_BOT_TOKEN = "8052262027:AAGdM8LVE3tHX9jt8OAyiDMFqUoGRHmdCLc"
CHAT_ID = "5008138452"  # Проверьте, что это правильный chat_id

def send_telegram_message(team_data):  # ✅ Изменено название аргумента, чтобы избежать конфликта
    text = f"""
📩 *Новая заявка*  
🏆 *Команда:* `{team_data['name']}`  
🌍 *Город:* `{team_data['city']}`  
🏫 *Учебное заведение:* `{team_data['institution']}`  
📧 *Контакт:* `{team_data['contact_info']}`  

👥 *Участники команды:*  
"""  
    for member in team_data['members']:
        text += f"   👤 `{member['full_name']}` - `{member['role']}` (📅 `{member['birth_date']}`)\n"

    text += f"""

💡 *Проект:* `{team_data['project']['name']}`  
📜 *Описание:* `{team_data['project']['description']}`  
🛠 *Технологии:* `{team_data['project']['technical_specs']}`  
🔎 *Доп. информация:* `{team_data['project']['additional_info']}`  
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {  # ✅ Изменено название переменной
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)  # ✅ Теперь нет конфликта с `data`
    
    if response.status_code == 200:
        print("✅ Сообщение успешно отправлено!")
    else:
        print(f"❌ Ошибка {response.status_code}: {response.text}")

# Тестовая отправка
team_data = {  # ✅ Изменено название переменной
    "name": "кцуеукеукенукн",
    "city": "Ташкент",
    "institution": "Ташкентский университет информационных технологий",
    "contact_info": "techpioneers@example.com",
    "members": [
        {
            "full_name": "Алексей Смирнов",
            "birth_date": "1999-07-12",
            "role": "Backend-разработчик"
        },
        {
            "full_name": "Мария Коваль",
            "birth_date": "2001-02-25",
            "role": "Frontend-разработчик"
        },
        {
            "full_name": "Олег Назаров",
            "birth_date": "2000-11-30",
            "role": "Дизайнер UI/UX"
        }
    ],
    "project": {
        "name": "рапрапрпр",
        "description": "Система умного города с интеграцией ИИ для оптимизации трафика и управления ресурсами.",
        "technical_specs": "Python, Django, React, PostgreSQL, AI/ML",
        "additional_info": "Проект включает анализ данных и интеграцию IoT-устройств"
    }
}

send_telegram_message(team_data)  # ✅ Передаём исправленную переменную