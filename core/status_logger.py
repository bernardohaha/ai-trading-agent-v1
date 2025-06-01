import json


class StatusLogger:
    def __init__(self, file_name="agent_status.json"):
        self.file_name = file_name

    def update_status(self, position, entry_price, pnl, position_action):
        data = {
            "position": position,
            "entry_price": entry_price,
            "pnl": pnl,
            "position_action": position_action,
        }
        with open(self.file_name, "w") as f:
            json.dump(data, f)
