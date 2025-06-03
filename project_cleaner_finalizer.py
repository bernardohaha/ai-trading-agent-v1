import os
import shutil

# Diretórios e ficheiros que podemos eliminar da raiz
files_to_remove = [
    "migrate_to_package.py",
    "fix_imports_v2.py",
    "patchfinal_v6.py",
    "patchfinal_v7.py",
    "patchfinal.py",
    "auto_patcher_ai_trading_agent.py",
    "auto_patcher_v2_ai_trading_agent.py",
    "auto_patcher_v3.py",
    "auto_patcher_v4.py",
    "auto_patcher_v5.py",
    "launcher_master.py",
    "launcher_master_final.py",
    "__pycache__",
    "_patcher_backup__",
]

# Diretório atual (raiz do projeto)
base_dir = os.getcwd()

for file in files_to_remove:
    path = os.path.join(base_dir, file)
    if os.path.isfile(path):
        os.remove(path)
        print(f"✔ Ficheiro removido: {file}")
    elif os.path.isdir(path):
        shutil.rmtree(path)
        print(f"✔ Pasta removida: {file}")
    else:
        print(f"⚠ Não encontrado: {file} (pode já ter sido movido)")

print("\n🚀 Limpeza concluída. Projeto pronto para trabalhar.")
