# optimizer_engine.py

import pandas as pd
import itertools
from ai_trading_agent.core.profile_engine import ProfileEngine, ProfileConfig
from ai_trading_agent.core.backtesting_engine import BacktestingEngine
from ai_trading_agent.core.metrics_calculator import MetricsCalculator


class OptimizerEngine:
    def __init__(self, data, initial_balance=10000):
        self.data = data
        self.initial_balance = initial_balance

    def run_grid_search(self, name, risk_range, atr_range, trailing_range):
        results = []

        # Gerar todas as combinações de parâmetros
        for risk_per_trade, atr_multiplier, trailing_value in itertools.product(
            risk_range, atr_range, trailing_range
        ):
            # Configurar perfil temporário
            pe = ProfileEngine()
            profile = ProfileConfig(
                name=name,
                risk_per_trade=risk_per_trade,
                max_daily_loss=0.05,
                atr_multiplier=atr_multiplier,
                trailing_mode="percent",
                trailing_value=trailing_value,
            )
            pe.add_profile(profile)

            # Executar backtest
            backtester = BacktestingEngine(self.data, pe, name, self.initial_balance)
            backtester.run_backtest()

            metrics = MetricsCalculator(backtester.trade_results, self.initial_balance)

            results.append(
                {
                    "risk_per_trade": risk_per_trade,
                    "atr_multiplier": atr_multiplier,
                    "trailing_value": trailing_value,
                    "total_profit": metrics.total_profit,
                    "profit_factor": metrics.profit_factor(),
                    "max_drawdown": metrics.max_drawdown(),
                    "sharpe": metrics.sharpe_ratio(),
                    "expectancy": metrics.expectancy(),
                }
            )

        # Retorna tudo como DataFrame
        df_results = pd.DataFrame(results).sort_values(
            by="total_profit", ascending=False
        )
        return df_results
