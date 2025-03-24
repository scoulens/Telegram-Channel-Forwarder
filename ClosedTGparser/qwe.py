import re
import asyncio
from telethon import TelegramClient, events


SESSION_FILE = "my_session"


API_ID = 25902306
API_HASH = "9af1bf758eb39864e130be954f3cb265"


PHONE = '+79880930309'  # Замените на свой номер телефона (в международном формате)


SOURCE_CHANNEL_ID = -1002407248544  # ID 1
DESTINATION_CHANNEL_ID = -1002387235974  # ID 2

# ссыль
REPLACEMENT_LINK = "#qwerty"

# Инициализация клиента Telethon
client = TelegramClient(SESSION_FILE, api_id=API_ID, api_hash=API_HASH,
                        system_version='5.12.3 x64')

def replace_emojis(text):
    """🛑."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("🛑", text)

def modify_message(message: str) -> str:
    """
    Заменяет ссылки вида #что-то-там на REPLACEMENT_LINK и все смайлики на 🛑.
    """
    message = re.sub(r"#\w+", REPLACEMENT_LINK, message)
    message = replace_emojis(message)
    return message

@client.on(events.NewMessage(chats=SOURCE_CHANNEL_ID))
async def handler(event):
    print(f"Получено сообщение: {event.raw_text}")
    modified_text = modify_message(event.raw_text)
    await client.send_message(DESTINATION_CHANNEL_ID, modified_text)
    print(f"Отправлено сообщение: {modified_text}")

async def main():
    await client.start(phone=PHONE)
    print("Бот запущен и следит за сообщениями...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())