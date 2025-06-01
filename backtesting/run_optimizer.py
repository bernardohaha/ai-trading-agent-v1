# run_optimizer.py

import pandas as pd
from optimizer_engine import OptimizerEngine

# Carregar CSV histórico
df = pd.read_csv("historical_data.csv")

# Inicializar optimizer
optimizer = OptimizerEngine(df, initial_balance=10000)

# Definir ranges de parâmetros
risk_range = [0.01, 0.02, 0.03]
atr_range = [1.0, 1.2, 1.5]
trailing_range = [0.005, 0.01, 0.015]

# Correr otimização
results_df = optimizer.run_grid_search(
    "Scalping", risk_range, atr_range, trailing_range
)

# Mostrar top resultados
print(results_df.head(10))
