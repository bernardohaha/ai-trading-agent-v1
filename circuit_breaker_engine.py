import datetime


class CircuitBreakerEngine:
    def __init__(self, max_daily_loss_pct=0.05, max_consecutive_losses=5):
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_consecutive_losses = max_consecutive_losses
        self.daily_pnl = 0
        self.consecutive_losses = 0
        self.last_trade_result = 0
        self.today = datetime.date.today()

    def update_daily(self, pnl):
        self._check_new_day()

        self.daily_pnl += pnl
        self.last_trade_result = pnl

        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

    def _check_new_day(self):
        if datetime.date.today() != self.today:
            self.today = datetime.date.today()
            self.daily_pnl = 0
            self.consecutive_losses = 0

    def should_halt_trading(self, balance):
        max_loss_value = balance * self.max_daily_loss_pct

        if self.daily_pnl <= -max_loss_value:
            return (
                True,
                f"🔴 Daily Loss Limit hit: {self.daily_pnl:.2f} vs max {max_loss_value:.2f}",
            )

        if self.consecutive_losses >= self.max_consecutive_losses:
            return True, f"🔴 Consecutive Losses Limit hit: {self.consecutive_losses}"

        return False, ""
