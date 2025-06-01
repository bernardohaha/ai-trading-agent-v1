import os
import telegram
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()


class TelegramAlerts:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = telegram.Bot(token=self.bot_token)

    def send_message(self, message):
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as e:
            print(f"[Telegram Error]: {e}")
