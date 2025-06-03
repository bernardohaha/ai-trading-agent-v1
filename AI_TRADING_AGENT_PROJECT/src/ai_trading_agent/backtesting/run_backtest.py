import pandas as pd
from ai_trading_agent.core.profile_engine import ProfileEngine, ProfileConfig
from ai_trading_agent.core.backtesting_engine import BacktestingEngine


# 1️⃣ Carregar o CSV histórico
df = pd.read_csv("ai_trading_agent/data/historical_data.csv")

# 2️⃣ Definir os perfis (podes depois puxar os que quiseres)
scalping = ProfileConfig(
    name="Scalping",
    risk_per_trade=0.02,
    max_daily_loss=0.05,
    atr_multiplier=1.2,
    trailing_mode="percent",
    trailing_value=0.01,
)

# 3️⃣ Inicializar o ProfileEngine
pe = ProfileEngine()
pe.add_profile(scalping)

# 4️⃣ Inicializar o Backtester
backtester = BacktestingEngine(
    data=df, profile_engine=pe, profile_name="Scalping", initial_balance=10000
)

# 5️⃣ Correr o backtest
backtester.run_backtest()
