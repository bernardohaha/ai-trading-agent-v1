class PerformanceTracker:
    def __init__(self):
        self.trades = []

    def log_trade(self, pnl):
        self.trades.append(pnl)

    def get_report(self):
        total_trades = len(self.trades)
        wins = len([t for t in self.trades if t > 0])
        losses = len([t for t in self.trades if t <= 0])
        total_pnl = sum(self.trades)
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
        profit_factor = (
            (
                sum(t for t in self.trades if t > 0)
                / abs(sum(t for t in self.trades if t < 0))
            )
            if losses > 0
            else float("inf")
        )

        return {
            "Total Trades": total_trades,
            "Wins": wins,
            "Losses": losses,
            "Win Rate (%)": round(win_rate, 2),
            "Total PnL": round(total_pnl, 2),
            "Profit Factor": round(profit_factor, 2),
        }
