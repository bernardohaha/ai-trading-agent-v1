# app_backtest_profiles.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from profile_engine import ProfileEngine, ProfileConfig
from backtesting_engine import BacktestingEngine
from metrics_calculator import MetricsCalculator
from backtest_logger import BacktestLogger


# ----- Perfis Disponíveis -----


def init_profiles():
    scalping = ProfileConfig("Scalping", 0.02, 0.05, 1.2, "percent", 0.01)
    swing = ProfileConfig("Swing", 0.01, 0.04, 1.5, "percent", 0.015)
    trend = ProfileConfig("Trend", 0.005, 0.03, 2.0, "atr", 1.0)

    pe = ProfileEngine()
    pe.add_profile(scalping)
    pe.add_profile(swing)
    pe.add_profile(trend)
    return pe


# ----- Streamlit App -----

st.set_page_config(page_title="AI Agent Cripto - Profile Comparison", layout="wide")

st.title("📊 AI Agent Cripto — Comparação de Perfis")

uploaded_file = st.file_uploader("📂 Carrega o CSV de dados históricos:", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV carregado com sucesso!")

    pe = init_profiles()
    initial_balance = st.number_input("Saldo Inicial (USDT):", value=10000.0)

    if st.button("Executar Comparação de Perfis"):
        logger = BacktestLogger()  # Inicializa o logger
        results = []
        equity_curves = {}

        for profile_name in pe.profiles.keys():
            backtester = BacktestingEngine(df, pe, profile_name, initial_balance)
            backtester.run_backtest()

            metrics = MetricsCalculator(backtester.trade_results, initial_balance)

            results.append(
                {
                    "Profile": profile_name,
                    "Total Profit": metrics.total_profit,
                    "Trades": metrics.total_trades,
                    "Winrate": (metrics.wins / metrics.total_trades) * 100,
                    "Profit Factor": metrics.profit_factor(),
                    "Max Drawdown": metrics.max_drawdown(),
                    "Sharpe": metrics.sharpe_ratio(),
                    "Expectancy": metrics.expectancy(),
                }
            )

            logger.log_result(profile_name, metrics)
            equity_curves[profile_name] = metrics.equity_curve

        # Mostrar Tabela Resumida
        st.subheader("📈 Resultados Comparativos")
        st.dataframe(pd.DataFrame(results).round(2))

        # Gráfico de Equity Curve
        st.subheader("📊 Equity Curves por Perfil")
        plt.figure(figsize=(10, 5))
        for profile_name, curve in equity_curves.items():
            plt.plot(curve, label=profile_name)
        plt.xlabel("Trades")
        plt.ylabel("Balance (USDT)")
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)
