# position_sizer.py

import logging


class PositionSizer:
    def __init__(
        self,
        account_balance: float,
        risk_per_trade: float = 0.01,  # 1% default
        atr_multiplier: float = 1.5,  # mais conservador = menor posição
    ):
        self.account_balance = account_balance
        self.risk_per_trade = risk_per_trade
        self.atr_multiplier = atr_multiplier

        logging.basicConfig(level=logging.INFO)

    def calculate_size(self, atr_value: float, entry_price: float):
        if atr_value <= 0 or entry_price <= 0:
            logging.error("ATR ou Entry Price inválidos.")
            return 0

        # Ajustar o risco baseado na volatilidade
        adjusted_risk = atr_value * self.atr_multiplier
        dollar_risk = self.account_balance * self.risk_per_trade

        position_size = dollar_risk / adjusted_risk
        position_value = position_size * entry_price

        logging.info(
            f"📊 Calculado position size com ATR: {position_size:.4f} unidades ({position_value:.2f} USD)"
        )
        return position_size
