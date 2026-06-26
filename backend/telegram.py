import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send(message):
    if not TOKEN or not CHAT_ID:
        print("❌ Missing Telegram credentials")
        return

    url = f"https://api.telegram.org/8929367550:AAE2F25nG3Yu-PEJFJy3jfVh8kgLr-Q1vXg/sendMessage"

    try:
        res = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False
        }, timeout=10)

        if res.status_code != 200:
            print("❌ Telegram failed:", res.text)
        else:
            print("✅ Telegram sent")

    except Exception as e:
        print("❌ Telegram error:", str(e))