# metrics_calculator.py

import numpy as np
import pandas as pd


class MetricsCalculator:
    def __init__(self, trade_results: list, initial_balance: float):
        self.results = trade_results
        self.initial_balance = initial_balance

        self.total_profit = sum(self.results)
        self.total_trades = len(self.results)
        self.wins = len([r for r in self.results if r > 0])
        self.losses = len([r for r in self.results if r <= 0])
        self.equity_curve = self.calculate_equity_curve()

    def calculate_equity_curve(self):
        curve = [self.initial_balance]
        for r in self.results:
            curve.append(curve[-1] + r)
        return curve

    def profit_factor(self):
        gains = sum(r for r in self.results if r > 0)
        losses = abs(sum(r for r in self.results if r < 0))
        return gains / losses if losses > 0 else np.inf

    def max_drawdown(self):
        curve = np.array(self.equity_curve)
        peak = np.maximum.accumulate(curve)
        drawdown = (peak - curve) / peak
        return np.max(drawdown) * 100  # em %

    def sharpe_ratio(self, risk_free_rate=0):
        returns = np.diff(self.equity_curve)
        if len(returns) < 2:
            return 0
        return np.mean(returns - risk_free_rate) / np.std(returns) * np.sqrt(252)

    def expectancy(self):
        avg_win = np.mean([r for r in self.results if r > 0]) if self.wins > 0 else 0
        avg_loss = (
            np.mean([r for r in self.results if r <= 0]) if self.losses > 0 else 0
        )
        win_rate = self.wins / self.total_trades if self.total_trades > 0 else 0
        return (avg_win * win_rate) + (avg_loss * (1 - win_rate))

    def summary(self):
        print("------ Métricas ------")
        print(f"Total Profit: {self.total_profit:.2f} USD")
        print(f"Total Trades: {self.total_trades}")
        print(f"Winrate: {(self.wins / self.total_trades) * 100:.2f}%")
        print(f"Profit Factor: {self.profit_factor():.2f}")
        print(f"Max Drawdown: {self.max_drawdown():.2f}%")
        print(f"Sharpe Ratio: {self.sharpe_ratio():.2f}")
        print(f"Expectancy: {self.expectancy():.2f}")
