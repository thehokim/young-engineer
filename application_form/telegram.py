import requests
from .models import BotSettings

def get_bot_settings():
    settings = BotSettings.objects.first()  # Получаем первую запись
    if settings:
        return settings.chat_id, settings.bot_token
    return None, None

def upload_video_to_telegram(video_file):
    """ Загружает видео в Telegram и возвращает ссылку """
    chat_id, bot_token = get_bot_settings()
    
    if not chat_id or not bot_token:
        print("❌ Ошибка: Не настроен Chat ID или Bot Token!")
        return None

    url_video = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    files = {'video': video_file}
    data = {"chat_id": chat_id}

    response = requests.post(url_video, data=data, files=files)

    if response.status_code == 200:
        video_info = response.json()
        file_id = video_info["result"]["video"]["file_id"]
        return f"https://t.me/{chat_id}/{file_id}"  # ✅ Генерируем ссылку на видео
    else:
        print(f"❌ Ошибка загрузки видео: {response.status_code} - {response.text}")
        return None

def send_telegram_message(team_data, video_url=None):
    chat_id, bot_token = get_bot_settings()
    
    if not chat_id or not bot_token:
        print("❌ Ошибка: Не настроен Chat ID или Bot Token!")
        return

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

    # ✅ Отправляем текст
    url_text = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(url_text, data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

    if response.status_code == 200:
        print("✅ Сообщение успешно отправлено!")
    else:
        print(f"❌ Ошибка {response.status_code}: {response.text}")

    # ✅ Если есть ссылка на видео, отправляем её в чат
    if video_url:
        url_video_msg = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response_video = requests.post(url_video_msg, data={"chat_id": chat_id, "text": f"🎥 Видео: {video_url}", "parse_mode": "Markdown"})

        if response_video.status_code == 200:
            print("✅ Ссылка на видео успешно отправлена!")
        else:
            print(f"❌ Ошибка при отправке ссылки на видео: {response_video.status_code} - {response_video.text}")
