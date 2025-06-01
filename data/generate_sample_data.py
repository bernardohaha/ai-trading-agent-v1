import pandas as pd
import random

# Gerar 20 exemplos simulados
data = []

for i in range(20):
    entry = round(random.uniform(3.0, 4.0), 2)
    stop_loss = round(entry - random.uniform(0.15, 0.30), 2)
    atr = round(random.uniform(0.20, 0.40), 2)
    high = round(entry + random.uniform(0.10, 0.30), 2)
    exit_price = round(entry + random.uniform(-0.15, 0.30), 2)

    data.append(
        {
            "entry": entry,
            "stop_loss": stop_loss,
            "exit": exit_price,
            "atr": atr,
            "high": high,
        }
    )

df = pd.DataFrame(data)
df.to_csv("historical_data.csv", index=False)

print("✅ CSV gerado com sucesso: historical_data.csv")
