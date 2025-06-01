# backtesting_engine.py

import pandas as pd
from orchestrator import Orchestrator
from profile_engine import ProfileEngine, ProfileConfig
from metrics_calculator import MetricsCalculator  # <--- NOVO


class BacktestingEngine:
    def __init__(
        self,
        data: pd.DataFrame,
        profile_engine: ProfileEngine,
        profile_name: str,
        initial_balance: float,
    ):
        self.data = data
        self.profile_engine = profile_engine
        self.profile_name = profile_name
        self.initial_balance = initial_balance
        self.orchestrator = Orchestrator(
            self.initial_balance, self.profile_engine, self.profile_name
        )

        # Resultados
        self.balance = initial_balance
        self.trades = 0
        self.trade_results = []  # <--- NOVO

    def run_backtest(self):
        for index, row in self.data.iterrows():
            entry_price = row["entry"]
            stop_loss_price = row["stop_loss"]
            atr_value = row["atr"]
            highest_price = row["high"]  # para trailing stop simular

            trade_info = self.orchestrator.evaluate_trade(
                entry_price, stop_loss_price, atr_value, highest_price
            )

            if trade_info:
                simulated_exit = row["exit"]
                profit = (simulated_exit - entry_price) * trade_info["position_size"]

                self.orchestrator.risk_manager.register_trade_result(profit)
                self.balance = self.orchestrator.risk_manager.account_balance
                self.trade_results.append(profit)
                self.trades += 1

        self.show_results()

    def show_results(self):
        print("-------- Backtesting Resultados --------")
        print(f"Perfil: {self.profile_name}")
        print(f"Trades executados: {self.trades}")
        print(f"Novo saldo: {self.balance:.2f} USD")

        # Calcular métricas
        metrics = MetricsCalculator(self.trade_results, self.initial_balance)
        metrics.summary()
