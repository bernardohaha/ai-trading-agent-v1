import streamlit as st
import pandas as pd
import json
import os
from streamlit_autorefresh import st_autorefresh

# Ficheiros de log
PERFORMANCE_FILE = "performance_log.json"
TRADES_FILE = "trades_log.json"
STATUS_FILE = "agent_status.json"

# Auto refresh a cada 5 segundos
st_autorefresh(interval=5000, limit=None, key="dashboard_refresh")

st.title("AI Trading Agent - Live Dashboard")

# === Performance Geral ===
st.subheader("Resumo Atual de Performance")


def load_performance():
    if os.path.exists(PERFORMANCE_FILE):
        with open(PERFORMANCE_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "Total Trades": 0,
            "Wins": 0,
            "Losses": 0,
            "Win Rate (%)": 0,
            "Total PnL": 0,
            "Profit Factor": 0,
        }


perf = load_performance()

st.write(f"Total Trades: {perf['Total Trades']}")
st.write(f"Wins: {perf['Wins']}")
st.write(f"Losses: {perf['Losses']}")
st.write(f"Win Rate: {perf['Win Rate (%)']}%")
st.write(f"Total PnL: {perf['Total PnL']}")
st.write(f"Profit Factor: {perf['Profit Factor']}")

# === Equity Curve ===
st.subheader("Equity Curve")


def load_trades():
    if os.path.exists(TRADES_FILE):
        with open(TRADES_FILE, "r") as f:
            return json.load(f)
    else:
        return []


trades = load_trades()

if trades:
    pnl_series = pd.Series(trades)
    equity_curve = pnl_series.cumsum()
    st.line_chart(equity_curve)
else:
    st.write("Nenhuma operação registrada ainda.")

# === Estado Atual da Posição ===
st.subheader("Status Atual do Agente")


def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "position": "NONE",
            "entry_price": 0,
            "pnl": 0,
            "position_action": "WAITING",
        }


status = load_status()

st.write(f"Posição atual: {status['position']}")
st.write(f"Preço de entrada: {status['entry_price']}")
st.write(f"PnL parcial (floating): {status['pnl']}")
st.write(f"Estado interno do Manager: {status['position_action']}")
