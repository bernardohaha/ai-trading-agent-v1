import os
from ai_trading_agent.core.interfaces.telegram_alerts import TelegramAlerts
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()


class AlertSystem:
    def __init__(self):
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = TelegramAlerts()  # Usar a classe correta

    async def send_alert(
        self, message, zone, decision, support, resistance, price
    ):  # Marcar como assíncrono
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
            await self.bot.send_message(message=full_msg)  # Adicionar await
        except Exception as e:
            print(f"[Telegram Error]: {e}")

        # Print local para debugging também
        print(full_msg)
