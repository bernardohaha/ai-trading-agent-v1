# app_backtest.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from profile_engine import ProfileEngine, ProfileConfig
from backtesting_engine import BacktestingEngine
from metrics_calculator import MetricsCalculator

# -------- Perfis disponíveis --------


def init_profiles():
    scalping = ProfileConfig(
        name="Scalping",
        risk_per_trade=0.02,
        max_daily_loss=0.05,
        atr_multiplier=1.2,
        trailing_mode="percent",
        trailing_value=0.01,
    )
    swing = ProfileConfig(
        name="Swing",
        risk_per_trade=0.01,
        max_daily_loss=0.04,
        atr_multiplier=1.5,
        trailing_mode="percent",
        trailing_value=0.015,
    )
    trend = ProfileConfig(
        name="Trend",
        risk_per_trade=0.005,
        max_daily_loss=0.03,
        atr_multiplier=2.0,
        trailing_mode="atr",
        trailing_value=1.0,
    )

    pe = ProfileEngine()
    pe.add_profile(scalping)
    pe.add_profile(swing)
    pe.add_profile(trend)
    return pe


# -------- Streamlit App --------

st.set_page_config(page_title="AI Agent Cripto - Backtest Dashboard", layout="wide")

st.title("📊 AI Agent Cripto — Backtest Dashboard")

# Upload CSV
st.subheader("1️⃣ Carrega o ficheiro de dados históricos")
uploaded_file = st.file_uploader("Seleciona o CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Ficheiro carregado com sucesso!")

    st.subheader("2️⃣ Seleciona o Perfil de Trading")

    # Perfis
    pe = init_profiles()
    profiles = list(pe.profiles.keys())
    selected_profile = st.selectbox("Perfil:", profiles)

    st.subheader("3️⃣ Executar Backtest")

    initial_balance = st.number_input("Saldo Inicial (USDT):", value=10000.0)

    if st.button("Correr Backtest"):
        # Backtest
        backtester = BacktestingEngine(df, pe, selected_profile, initial_balance)
        backtester.run_backtest()

        # Métricas
        metrics = MetricsCalculator(backtester.trade_results, initial_balance)

        # Mostrar Resultados
        st.write("### 📈 Resultados do Backtest")
        st.write(f"Total Profit: {metrics.total_profit:.2f} USD")
        st.write(f"Total Trades: {metrics.total_trades}")
        st.write(f"Winrate: {(metrics.wins / metrics.total_trades) * 100:.2f}%")
        st.write(f"Profit Factor: {metrics.profit_factor():.2f}")
        st.write(f"Max Drawdown: {metrics.max_drawdown():.2f}%")
        st.write(f"Sharpe Ratio: {metrics.sharpe_ratio():.2f}")
        st.write(f"Expectancy: {metrics.expectancy():.2f}")

        # Equity Curve
        st.write("### 📊 Equity Curve")

        plt.figure(figsize=(10, 4))
        plt.plot(metrics.equity_curve, label="Equity Curve", color="blue")
        plt.xlabel("Trades")
        plt.ylabel("Balance (USDT)")
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)
