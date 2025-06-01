import yaml


class ConfigLoader:
    def __init__(self, file_path="config.yaml"):
        self.file_path = file_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.file_path, "r") as f:
            return yaml.safe_load(f)

    def get_scoring_config(self):
        return self.config.get("scoring", {})

    def get_position_manager_config(self):
        return self.config.get("position_manager", {})

    def get_safety_filter_config(self):
        return self.config.get("safety_filter", {})

    def get_circuit_breaker_config(self):
        return self.config.get("circuit_breaker", {})
