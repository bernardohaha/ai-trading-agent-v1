import json
import os


class CircuitBreaker:
    def __init__(self, config, pnl_file="performance_log.json"):
        self.pnl_file = pnl_file
        self.max_daily_loss = config["max_daily_loss"]
        self.max_consecutive_losses = config["max_consecutive_losses"]

    def load_pnl_data(self):
        if os.path.exists(self.pnl_file):
            with open(self.pnl_file, "r") as f:
                return json.load(f)
        else:
            return {
                "Total Trades": 0,
                "Wins": 0,
                "Losses": 0,
                "Win Rate (%)": 0,
                "Total PnL": 0,
                "Profit Factor": 0,
            }

    def check(self):
        data = self.load_pnl_data()

        total_pnl = data["Total PnL"]
        losses = data["Losses"]

        if total_pnl <= -self.max_daily_loss:
            return False, f"Daily PnL limit reached: {total_pnl}"

        if losses >= self.max_consecutive_losses:
            return False, f"Max consecutive losses reached: {losses}"

        return True, "Circuit Breaker OK"
