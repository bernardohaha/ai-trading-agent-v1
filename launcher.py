import sys
import pathlib

# Definir o path raiz do projeto
ROOT_PATH = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(ROOT_PATH))

# Opcional: podes logar que o ambiente foi carregado
print("\n[AI TRADING AGENT] Ambiente carregado com sucesso!")
print("[AI TRADING AGENT] Diretório raiz:", ROOT_PATH)

# Exemplo de como podes importar qualquer módulo:
# from frontend import app
# from core import decision_engine
# from backtesting import app_backtest

# Podes agora correr qualquer módulo normalmente:
# Exemplo:
# python frontend/run_agent.py
# python backtesting/app_backtest.py
# python frontend/app.py (caso uses o streamlit run)
