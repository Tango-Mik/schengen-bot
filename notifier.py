import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def notify(message):
    url = f"https://api.telegram.org/bot8626046136:AAHa-v95IDRzXJ2Zpbkf_-d_QzXBfc4KoJY/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)
