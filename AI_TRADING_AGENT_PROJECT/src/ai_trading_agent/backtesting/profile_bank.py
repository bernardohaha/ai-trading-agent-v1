# profile_bank.py

import json
import os


class ProfileBank:
    def __init__(self, filename="profile_bank.json"):
        self.filename = filename
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_profile(self, name, profile_data):
        self.data[name] = profile_data
        self.save()

    def remove_profile(self, name):
        if name in self.data:
            del self.data[name]
            self.save()

    def get_profile(self, name):
        return self.ai_trading_agent.data.get(name)

    def list_profiles(self):
        return list(self.ai_trading_agent.data.keys())

    def get_all_profiles(self):
        return self.data
