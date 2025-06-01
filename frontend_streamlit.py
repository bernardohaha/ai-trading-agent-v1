import streamlit as st
import pandas as pd
import json
import os

from streamlit_autorefresh import st_autorefresh

# Simulador de leitura de performance (no futuro vais ligar ao verdadeiro log do agent)
PERFORMANCE_FILE = "performance_log.json"


# Função para carregar os dados de performance
def load_performance():
    if os.path.exists(PERFORMANCE_FILE):
        with open(PERFORMANCE_FILE, "r") as f:
            data = json.load(f)
        return data
    else:
        return {
            "Total Trades": 0,
            "Wins": 0,
            "Losses": 0,
            "Win Rate (%)": 0,
            "Total PnL": 0,
            "Profit Factor": 0,
        }


st.title("AI Trading Agent - Live Dashboard")

# Auto refresh a cada 5 segundos
st_autorefresh(interval=5000, limit=None, key="dashboard_refresh")

data = load_performance()

st.subheader("Resumo Atual de Performance")
st.write(f"Total Trades: {data['Total Trades']}")
st.write(f"Wins: {data['Wins']}")
st.write(f"Losses: {data['Losses']}")
st.write(f"Win Rate: {data['Win Rate (%)']}%")
st.write(f"Total PnL: {data['Total PnL']}")
st.write(f"Profit Factor: {data['Profit Factor']}")
