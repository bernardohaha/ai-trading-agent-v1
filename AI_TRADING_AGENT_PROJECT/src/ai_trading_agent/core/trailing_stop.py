# trailing_stop.py

import logging


class TrailingStop:
    def __init__(
        self,
        mode: str = "percent",  # "percent" ou "atr"
        trailing_value: float = 0.02,  # Ex.: 2% ou atr_multiplier
        atr_value: float = None,
    ):
        self.mode = mode
        self.trailing_value = trailing_value
        self.atr_value = atr_value

        logging.basicConfig(level=logging.INFO)

    def calculate_stop(self, entry_price: float, highest_price: float):
        if entry_price <= 0 or highest_price <= 0:
            logging.error("Entry price ou highest price inválidos.")
            return None

        if self.mode == "percent":
            trail_distance = highest_price * self.trailing_value
        elif self.mode == "atr":
            if self.atr_value is None or self.atr_value <= 0:
                logging.error("ATR inválido.")
                return None
            trail_distance = self.atr_value * self.trailing_value
        else:
            logging.error("Modo de trailing inválido.")
            return None

        trailing_stop_price = highest_price - trail_distance

        logging.info(f"📉 Trailing Stop recalculado: {trailing_stop_price:.4f}")
        return trailing_stop_price

    def update_highest_price(self, current_price: float, previous_high: float):
        return max(current_price, previous_high)
