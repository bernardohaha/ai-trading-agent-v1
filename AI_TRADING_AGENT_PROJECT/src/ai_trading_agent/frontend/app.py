# app.py

import streamlit as st
from ai_trading_agent.ai_trading_agent.frontend.ai_trading_agent.strategies.profile_engine import ProfileEngine, ProfileConfig
from ai_trading_agent.ai_trading_agent.frontend.ai_trading_agent.core.orchestrator import Orchestrator

# ------- Inicializar Perfis -------- #


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


# ------- Streamlit Interface -------- #

st.set_page_config(page_title="AI Agent Cripto Control Center", layout="centered")

st.title("💰 AI Agent Cripto - Control Center V1")

# Inicializar Perfis
profile_engine = init_profiles()
profile_names = list(profile_engine.profiles.keys())

# Selecionar perfil ativo
selected_profile = st.selectbox("Seleciona o Perfil de Trading:", profile_names)

profile_engine.set_active_profile(selected_profile)
active_config = profile_engine.get_active_config()

# Mostrar configurações do perfil
st.subheader("Configuração do Perfil Ativo:")
st.write(active_config)

# Inputs de trade
st.subheader("Simular Trade:")

account_balance = st.number_input(
    "Account Balance (USDT):", min_value=0.0, value=10000.0
)
entry_price = st.number_input("Entry Price:", min_value=0.0, value=3.50)
stop_loss_price = st.number_input("Stop Loss Price:", min_value=0.0, value=3.30)
atr_value = st.number_input("ATR Value:", min_value=0.0, value=0.25)
highest_price = st.number_input("Highest Price Reached:", min_value=0.0, value=3.70)

if st.button("Calcular Trade"):
    orchestrator = Orchestrator(account_balance, profile_engine, selected_profile)
    trade_info = orchestrator.evaluate_trade(
        entry_price, stop_loss_price, atr_value, highest_price
    )

    if trade_info:
        st.success("✅ Trade Aprovado")
        st.write(f"Position Size: {trade_info['position_size']:.4f} unidades")
        st.write(f"Trailing Stop: {trade_info['trailing_stop']:.4f}")
    else:
        st.error("🚫 Trade Bloqueado pelo Risk Manager.")
