# risk_manager.py

import logging
from datetime import datetime, timedelta


class RiskManager:
    def __init__(
        self,
        account_balance: float,
        risk_per_trade: float = 0.01,  # 1% de risco por trade
        max_daily_loss: float = 0.05,  # 5% de risco diário
        trade_history: list = None,
        daily_loss_reset_hour: int = 0,  # Reset diário à meia-noite UTC por default
    ):
        self.account_balance = account_balance
        self.risk_per_trade = risk_per_trade
        self.max_daily_loss = max_daily_loss
        self.trade_history = trade_history if trade_history else []

        self.daily_loss = 0.0
        self.daily_loss_reset_time = self._get_reset_time(daily_loss_reset_hour)

        logging.basicConfig(level=logging.INFO)

    def _get_reset_time(self, reset_hour):
        now = datetime.utcnow()
        return now.replace(hour=reset_hour, minute=0, second=0, microsecond=0)

    def reset_daily_loss_if_needed(self):
        now = datetime.utcnow()
        if now >= self.daily_loss_reset_time + timedelta(days=1):
            self.daily_loss = 0.0
            self.daily_loss_reset_time = self._get_reset_time(
                self.daily_loss_reset_time.hour
            )
            logging.info("✅ Daily loss reset efetuado.")

    def check_daily_loss_limit(self):
        self.reset_daily_loss_if_needed()
        allowed_daily_loss = self.account_balance * self.max_daily_loss
        if self.daily_loss >= allowed_daily_loss:
            logging.warning("🚫 Limite diário de perda atingido. Trading suspenso.")
            return False
        return True

    def calculate_position_size(self, entry_price: float, stop_loss_price: float):
        if entry_price <= stop_loss_price:
            logging.error(
                "Erro: o preço de entrada deve ser superior ao preço de stop-loss (posição long)."
            )
            return 0

        risk_amount = self.account_balance * self.risk_per_trade
        position_size = risk_amount / (entry_price - stop_loss_price)
        position_value = position_size * entry_price

        # Logging
        logging.info(
            f"📊 Calculado position size: {position_size:.4f} unidades ({position_value:.2f} USD)"
        )

        return position_size

    def register_trade_result(self, trade_profit_loss: float):
        self.trade_history.append(trade_profit_loss)
        self.daily_loss += max(
            -trade_profit_loss, 0
        )  # Apenas contabiliza perdas no daily loss
        self.account_balance += trade_profit_loss

        # Logging
        logging.info(f"💰 Resultado registado: {trade_profit_loss:.2f} USD")
        logging.info(f"💼 Novo account balance: {self.account_balance:.2f} USD")
        logging.info(f"📉 Daily loss atualizado: {self.daily_loss:.2f} USD")

    def can_open_trade(self, entry_price: float, stop_loss_price: float):
        if not self.check_daily_loss_limit():
            return False

        position_size = self.calculate_position_size(entry_price, stop_loss_price)
        if position_size == 0:
            logging.warning("🚫 Position size inválido. Trade não será aberto.")
            return False

        return True
