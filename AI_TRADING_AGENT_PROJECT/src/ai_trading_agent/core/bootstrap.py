from ai_trading_agent.config.profiles_config import load_profiles
from ai_trading_agent.core.profile_engine import ProfileEngine


class TradingSystem:
    def __init__(self):
        self.profile_engine = ProfileEngine()
        self.load_profiles()

    def load_profiles(self):
        profiles = load_profiles()
        for profile in profiles:
            self.profile_engine.add_profile(profile)

        # Definir perfil ativo default (podes mudar depois dinamicamente)
        self.profile_engine.set_active_profile("Scalping")

    def get_active_profile(self):
        return self.profile_engine.get_active_config()
