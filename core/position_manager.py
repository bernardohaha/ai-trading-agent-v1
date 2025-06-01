class PositionManager:
    def __init__(self, entry_price, config):
        self.entry_price = entry_price
        self.hold_candles = config["hold_candles"]
        self.take_profit = config["take_profit"]
        self.stop_loss = config["stop_loss"]
        self.candles_held = 0

    def update(self, current_price):
        self.candles_held += 1

        pnl_percentage = (current_price - self.entry_price) / self.entry_price

        if pnl_percentage >= self.take_profit:
            return "EXIT TAKE PROFIT"
        elif pnl_percentage <= -self.stop_loss:
            return "EXIT STOP LOSS"
        elif self.candles_held >= self.hold_candles:
            return "CHECK FOR EXIT"
        else:
            return "HOLD"
