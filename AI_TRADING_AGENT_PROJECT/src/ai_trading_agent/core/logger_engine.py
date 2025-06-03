import json
import logging
from ai_trading_agent.ai_trading_agent.interfaces.datetime import datetime


class LoggerEngine:
    def __init__(self, log_file="ai_agent_logs.json"):
        self.log_file = log_file
        logging.basicConfig(level=logging.INFO)

    def log_event(self, event_type, data):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data,
        }
        self._save_to_file(log_entry)
        logging.info(json.dumps(log_entry))

    def _save_to_file(self, log_entry):
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logging.error(f"Falha ao escrever log: {e}")
