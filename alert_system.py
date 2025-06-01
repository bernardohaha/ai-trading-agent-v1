import datetime


class AlertSystem:
    def __init__(self):
        pass  # Podemos depois ligar API de Telegram ou Email aqui

    def send_alert(self, message, zone, decision, support, resistance, price):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n=== ALERTA ({timestamp}) ===")
        print(f"Mensagem: {message}")
        print(f"Zona atual: {zone}")
        print(f"Decisão AI: {decision}")
        print(f"Preço Atual: {price:.2f}")
        print(f"Suporte: {support}")
        print(f"Resistência: {resistance}")
        print(f"=============================\n")
