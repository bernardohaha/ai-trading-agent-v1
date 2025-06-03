import json
import os


class StatusLogger:
    def __init__(self, file_name="agent_status.json"):
        self.file_path = os.path.join(
            "AI_TRADING_AGENT_PROJECT", "ai_trading_agent", "data", file_name
        )
        self.status_data = {}  # Adicionar um dicionário para guardar o estado

    def update(self, data):  # Alterar o nome do método e aceitar um dicionário
        self.status_data.update(data)  # Atualizar o dicionário interno
        self._save_status()  # Guardar o estado no ficheiro

    def _save_status(self):  # Método privado para guardar no ficheiro
        with open(self.file_path, "w") as f:
            json.dump(
                self.status_data, f, indent=4
            )  # Guardar o dicionário completo com indentação
