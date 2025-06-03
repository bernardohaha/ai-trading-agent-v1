import json


class PerformanceTracker:
    def __init__(self, log_file="performance_log.json", trades_file="trades_log.json"):
        self.trades = []
        self.log_file = log_file
        self.trades_file = trades_file

    def log_trade(self, pnl):
        self.trades.append(pnl)
        self.save_performance()
        self.save_trades()

    def update(self, profile_name, decision):
        """
        Novo método para integração com o ProfileRunner
        (mesmo que neste momento ainda não recebemos PnL)
        """
        entry = {"profile": profile_name, "decision": decision}
        # Apenas fazemos log visual por enquanto (pode-se expandir depois)
        print(f"📊 [PERFORMANCE] {profile_name}: {decision}")

        # Se quiseres, poderíamos mais tarde gravar estas decisões num log próprio
        # Exemplo: self.trades.append(entry)

    def save_performance(self):
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

        data = {
            "Total Trades": total_trades,
            "Wins": wins,
            "Losses": losses,
            "Win Rate (%)": round(win_rate, 2),
            "Total PnL": round(total_pnl, 2),
            "Profit Factor": round(profit_factor, 2),
        }

        with open(self.log_file, "w") as f:
            json.dump(data, f)

    def save_trades(self):
        with open(self.trades_file, "w") as f:
            json.dump(self.trades, f)

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
