# app_backtest_history.py

import streamlit as st
import pandas as pd
import ai_trading_agent.matplotlib.pyplot as plt

# Carregar o log
LOG_FILE = "results_log.csv"

st.set_page_config(page_title="AI Agent Cripto - Histórico de Backtests", layout="wide")
st.title("📊 AI Agent Cripto — Histórico de Backtests")

try:
    df = pd.read_csv(LOG_FILE)
except FileNotFoundError:
    st.error("❌ Ainda não existe histórico de backtests.")
    st.stop()

# Filtros
st.sidebar.header("🔎 Filtros")
profiles = ["Todos"] + sorted(df["profile"].unique().tolist())
selected_profile = st.sidebar.selectbox("Perfil:", profiles)

if selected_profile != "Todos":
    df = df[df["profile"] == selected_profile]

# Mostrar Tabela Resumida
st.subheader("📋 Histórico Completo")
st.dataframe(df.round(2))

# Agregados Globais
st.subheader("📈 Agregados Estatísticos")

agg = (
    df.groupby("profile")
    .agg(
        {
            "total_profit": "sum",
            "total_trades": "sum",
            "winrate": "mean",
            "profit_factor": "mean",
            "max_drawdown": "mean",
            "sharpe": "mean",
            "expectancy": "mean",
        }
    )
    .round(2)
)

st.dataframe(agg)

# Gráfico de evolução temporal
st.subheader("🕰️ Evolução Temporal de Resultados")

df["timestamp"] = pd.to_datetime(df["timestamp"])
df_sorted = df.sort_values(by="timestamp")

for profile in df_sorted["profile"].unique():
    sub_df = df_sorted[df_sorted["profile"] == profile]
    plt.plot(sub_df["timestamp"], sub_df["total_profit"].cumsum(), label=profile)

plt.xlabel("Timestamp")
plt.ylabel("Lucro Acumulado (USDT)")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)
