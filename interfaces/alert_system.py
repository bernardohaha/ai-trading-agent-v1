import os
from telegram import Bot
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()


class AlertSystem:
    def __init__(self):
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = Bot(token=self.telegram_token)

    def send_alert(self, message, zone, decision, support, resistance, price):
        alert_msg = f"""
🟢 [AI Trading Agent] Novo Sinal 📊

📈 Zona Atual: {zone}
🎯 Decisão: {decision}
💰 Preço Atual: {price}

🔻 Suporte: {support}
🔺 Resistência: {resistance}

"""
        full_msg = f"{message}\n{alert_msg}"

        # Enviar para o Telegram
        try:
            self.bot.send_message(chat_id=self.telegram_chat_id, text=full_msg)
        except Exception as e:
            print(f"[Telegram Error]: {e}")

        # Print local para debugging também
        print(full_msg)
