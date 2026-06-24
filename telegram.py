import httpx
from dotenv import load_dotenv
import os

# Load credentials from the local environment setup
load_dotenv()


ALERT_BOT_TOKEN = os.getenv("ALERT_BOT_TOKEN", "the_PERSONAL_BOT_TOKEN")       
MY_PERSONAL_CHAT_ID = os.getenv("MY_PERSONAL_CHAT_ID", "the_PERSONAL_CHAT_ID") 

async def send_personal_telegram_async(message):
    url = f"https://api.telegram.org/bot{ALERT_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": MY_PERSONAL_CHAT_ID, "text": f"🔥 **CRITICAL F1 SLOT ALERT** 🔥\n\n`{message}`", "parse_mode": "Markdown"}
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, timeout=4.0)
    except Exception as e: 
        print(f"Failed to send personal Telegram message: {e}")