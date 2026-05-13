import requests

# ✅ Paste your NEW bot token between the quotes
BOT_TOKEN = "8626046136:AAHa-v95IDRzXJ2Zpbkf_-d_QzXBfc4KoJY"

# ✅ Paste your chat ID between the quotes
CHAT_ID = "1089668720"

def notify(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

# ✅ TEMPORARY TEST MESSAGE
