# profile_engine.py

import logging


class ProfileConfig:
    """
    Define a configuração completa de cada perfil.
    """

    def __init__(
        self,
        name,
        risk_per_trade,
        max_daily_loss,
        atr_multiplier,
        trailing_mode,
        trailing_value,
    ):
        self.name = name
        self.risk_per_trade = risk_per_trade
        self.max_daily_loss = max_daily_loss
        self.atr_multiplier = atr_multiplier
        self.trailing_mode = trailing_mode  # 'percent' ou 'atr'
        self.trailing_value = trailing_value

    def get_config(self):
        return {
            "name": self.name,
            "risk_per_trade": self.risk_per_trade,
            "max_daily_loss": self.max_daily_loss,
            "atr_multiplier": self.atr_multiplier,
            "trailing_mode": self.trailing_mode,
            "trailing_value": self.trailing_value,
        }


class ProfileEngine:
    """
    Motor de seleção de perfil e entrega de configs.
    """

    def __init__(self):
        self.profiles = {}
        self.active_profile = None

        logging.basicConfig(level=logging.INFO)

    def add_profile(self, profile: ProfileConfig):
        self.profiles[profile.name] = profile
        logging.info(f"Perfil adicionado: {profile.name}")

    def set_active_profile(self, profile_name: str):
        if profile_name in self.profiles:
            self.active_profile = self.profiles[profile_name]
            logging.info(f"Perfil ativo: {profile_name}")
        else:
            logging.warning(f"Perfil {profile_name} não encontrado.")

    def get_active_config(self):
        if self.active_profile:
            return self.active_profile.get_config()
        else:
            logging.warning("Nenhum perfil ativo.")
            return None
