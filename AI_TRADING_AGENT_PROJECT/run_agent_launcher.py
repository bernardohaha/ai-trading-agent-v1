import sys
import os

# Adiciona automaticamente o diretório src/ ao sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

# Logger opcional (só para controlo visual)
print("\n✅ [AI TRADING AGENT]: Ambiente carregado com sucesso!")
print(f"📂 Diretório raiz: {current_dir}")
print(f"📂 Diretório src: {src_dir}")

# Agora podes importar qualquer módulo do projeto
# Exemplo: arrancar o multiprofile_engine
from ai_trading_agent import multiprofile_engine

if __name__ == "__main__":
    multiprofile_engine.main()  # <-- Só funciona se multiprofile_engine.py tiver um main()
