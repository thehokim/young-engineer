import requests
from django.core.files.uploadedfile import UploadedFile

BOT_TOKEN = "8052262027:AAGD..."  # Укороченный токен
CHAT_IDS = [5008138452, 165378299, 68177994, 286042360]

def upload_file_to_telegram(file: UploadedFile):
    """Uploads a file to Telegram and returns the file_id."""
    if not file:
        print("❌ Файл отсутствует")
        return None

    file_extension = file.name.split(".")[-1].lower()

    # Определяем, какой метод API использовать
    file_types = {
        "photo": ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
        "video": ["mp4", "mov", "avi", "mkv"],
        "document": ["pdf", "doc", "docx", "xls", "xlsx", "txt"],
    }

    file_type = next((ftype for ftype, exts in file_types.items() if file_extension in exts), None)

    if not file_type:
        print(f"❌ Неподдерживаемый формат файла: {file_extension}")
        return None

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/send{file_type.capitalize()}"
    first_chat_id = CHAT_IDS[0]
    files = {file_type: (file.name, file.file)}
    data = {"chat_id": first_chat_id}

    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        file_info = response.json()
        if not file_info.get("ok"):
            print(f"❌ Ошибка Telegram API: {file_info}")
            return None

        file_id = file_info["result"].get("file_id")
        if not file_id:
            print(f"❌ Ошибка: Telegram не вернул file_id: {file_info}")
            return None

        print(f"✅ {file_extension.upper()} файл загружен в чат {first_chat_id}")

        # Рассылка в другие чаты
        for chat_id in CHAT_IDS[1:]:
            response = requests.post(url, data={"chat_id": chat_id, file_type: file_id})
            if response.status_code == 200:
                print(f"✅ Файл отправлен в чат {chat_id}")
            else:
                print(f"❌ Ошибка отправки в чат {chat_id}: {response.status_code} - {response.text}")

        return file_id
    else:
        print(f"❌ Ошибка загрузки файла в чат {first_chat_id}: {response.status_code} - {response.text}")
        return None


def send_telegram_message(team_data):
    """Sends team information to Telegram chats."""
    text = f"""
📩 *Новая заявка*
🏆 *Команда:* `{team_data['name']}`
🌍 *Город:* `{team_data['city']}`
🏫 *Учебное заведение:* `{team_data['institution']}`
📧 *Контакт:* `{team_data['contact_info']}`

👥 *Участники команды:*
""" + "\n".join(
        [f"   👤 `{member['full_name']}` - `{member['role']}` (📅 `{member['birth_date']}`)"
         for member in team_data["members"]]
    ) + f"""

💡 *Проект:* `{team_data['project']['name']}`
📜 *Описание:* `{team_data['project']['description']}`
🛠 *Технологии:* `{team_data['project']['technical_specs']}`
🔎 *Доп. информация:* `{team_data['project']['additional_info']}`
"""

    url_text = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:
        response = requests.post(
            url_text,
            data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        )
        if response.status_code == 200:
            print(f"✅ Сообщение отправлено в чат {chat_id}")
        else:
            print(f"❌ Ошибка отправки в чат {chat_id}: {response.status_code} - {response.text}")
