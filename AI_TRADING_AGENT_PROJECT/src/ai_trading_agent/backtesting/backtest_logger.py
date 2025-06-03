# backtest_logger.py

import pandas as pd
from ai_trading_agent.ai_trading_agent.backtesting.datetime import datetime
import os


class BacktestLogger:
    def __init__(self, log_file="results_log.csv"):
        self.log_file = log_file

        if not os.path.exists(self.log_file):
            self._create_log()

    def _create_log(self):
        columns = [
            "timestamp",
            "profile",
            "total_profit",
            "total_trades",
            "winrate",
            "profit_factor",
            "max_drawdown",
            "sharpe",
            "expectancy",
        ]
        df = pd.DataFrame(columns=columns)
        df.to_csv(self.log_file, index=False)

    def log_result(self, profile_name, metrics):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "profile": profile_name,
            "total_profit": round(metrics.total_profit, 2),
            "total_trades": metrics.total_trades,
            "winrate": round((metrics.wins / metrics.total_trades) * 100, 2),
            "profit_factor": round(metrics.profit_factor(), 2),
            "max_drawdown": round(metrics.max_drawdown(), 2),
            "sharpe": round(metrics.sharpe_ratio(), 2),
            "expectancy": round(metrics.expectancy(), 2),
        }

        df = pd.DataFrame([entry])
        df.to_csv(self.log_file, mode="a", header=False, index=False)
