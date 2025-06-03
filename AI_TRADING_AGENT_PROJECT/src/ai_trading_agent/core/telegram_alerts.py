import os
import telegram
from telegram import Bot
from dotenv import load_dotenv
import asyncio

# Carregar variáveis do .env
load_dotenv()


class TelegramAlerts:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.bot_token:
            print("[TelegramAlerts Error]: TELEGRAM_BOT_TOKEN not set in .env")
            self.bot = None
        else:
            self.bot = Bot(token=self.bot_token)

        if not self.chat_id:
            print("[TelegramAlerts Error]: TELEGRAM_CHAT_ID not set in .env")
            self.chat_id = None

    def send_alert(self, message):
        if not self.bot or not self.chat_id:
            print(f"[ALERT]: {message}")
            return

        try:
            # Forçar o asyncio loop para usar o send_message
            asyncio.run(self.bot.send_message(chat_id=self.chat_id, text=message))
        except Exception as e:
            print(f"[Telegram Error]: {e}")
