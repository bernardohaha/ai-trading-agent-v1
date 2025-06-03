# app_optimizer.py

import streamlit as st
import pandas as pd
import ai_trading_agent.matplotlib.pyplot as plt

from ai_trading_agent.ai_trading_agent.backtesting.ai_trading_agent.backtesting.optimizer_engine import OptimizerEngine
from ai_trading_agent.ai_trading_agent.backtesting.ai_trading_agent.strategies.profile_engine import ProfileEngine
from ai_trading_agent.ai_trading_agent.backtesting.ai_trading_agent.strategies.auto_profile_generator import AutoProfileGenerator

# Configuração inicial do Streamlit
st.set_page_config(page_title="AI Agent Cripto - Optimizer Lab", layout="wide")
st.title("🤖 AI Agent Cripto — Optimizer Lab")

# Upload CSV
uploaded_file = st.file_uploader("📂 Carrega o CSV de dados históricos:", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV carregado com sucesso!")

    st.header("⚙️ Configuração do Grid Search")

    # Ranges dos parâmetros
    risk_range = st.slider("Risk per Trade (min/max)", 0.005, 0.05, (0.01, 0.03), 0.005)
    atr_range = st.slider("ATR Multiplier (min/max)", 1.0, 3.0, (1.2, 2.0), 0.1)
    trailing_range = st.slider(
        "Trailing Value (min/max)",
        0.001,
        0.05,
        (0.005, 0.015),
        step=0.005,
        format="%.3f",
    )

    # Grid Step (resolução de busca)
    grid_step = st.selectbox("Precisão da Busca", [1, 3, 5, 10])

    # Gerar os grids
    risk_values = [
        round(x, 3)
        for x in list(
            pd.Series(
                pd.interval_range(risk_range[0], risk_range[1], periods=grid_step).mid
            )
        )
    ]
    atr_values = [
        round(x, 2)
        for x in list(
            pd.Series(
                pd.interval_range(atr_range[0], atr_range[1], periods=grid_step).mid
            )
        )
    ]
    trailing_values = [
        round(x, 3)
        for x in list(
            pd.Series(
                pd.interval_range(
                    trailing_range[0], trailing_range[1], periods=grid_step
                ).mid
            )
        )
    ]

    st.write(
        f"🔎 Total de combinações: {len(risk_values) * len(atr_values) * len(trailing_values)}"
    )

    # Inicializamos o session state para guardar resultados
    if "results_df" not in st.session_state:
        st.session_state.results_df = None

    if st.button("🚀 Iniciar Otimização"):
        optimizer = OptimizerEngine(df, initial_balance=10000)
        results_df = optimizer.run_grid_search(
            "Scalping", risk_values, atr_values, trailing_values
        )
        st.session_state.results_df = results_df  # Guardar no estado

    # Só mostramos os resultados se já houver otimização feita
    if st.session_state.results_df is not None:
        results_df = st.session_state.results_df

        st.success("✅ Otimização concluída!")
        st.write("📊 Top 20 resultados:")
        st.dataframe(results_df.head(20).round(3))

        # Gráfico rápido de lucro vs drawdown
        st.subheader("📈 Lucro vs Drawdown")
        plt.figure(figsize=(10, 5))
        plt.scatter(results_df["max_drawdown"], results_df["total_profit"], c="blue")
        plt.xlabel("Max Drawdown (%)")
        plt.ylabel("Total Profit (USDT)")
        plt.grid(True)
        st.pyplot(plt)

        # Melhor setup encontrado
        best_row = results_df.iloc[0]

        st.write("🔧 Melhor Setup Encontrado:")
        st.json(
            {
                "risk_per_trade": best_row["risk_per_trade"],
                "atr_multiplier": best_row["atr_multiplier"],
                "trailing_value": best_row["trailing_value"],
            }
        )

        # Criação de novo perfil
        new_profile_name = st.text_input(
            "Nome do Novo Perfil:", value="OptimizedProfile"
        )

        if st.button("➕ Adicionar Novo Perfil"):
            profile_engine = ProfileEngine()
            generator = AutoProfileGenerator(profile_engine)
            new_profile = generator.generate_profile_from_row(
                new_profile_name, best_row
            )
            st.success(f"✅ Perfil '{new_profile_name}' adicionado com sucesso!")
