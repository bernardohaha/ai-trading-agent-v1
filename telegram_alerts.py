from telegram import Bot


class TelegramAlerts:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    def send(self, message):
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as e:
            print(f"Erro ao enviar alerta Telegram: {e}")
