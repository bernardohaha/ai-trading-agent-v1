# auto_profile_generator.py

from profile_engine import ProfileConfig


class AutoProfileGenerator:
    def __init__(self, profile_engine):
        self.profile_engine = profile_engine

    def generate_profile_from_row(self, name, row):
        profile = ProfileConfig(
            name=name,
            risk_per_trade=row["risk_per_trade"],
            max_daily_loss=0.05,  # Podes ajustar se quiseres parametrizar no futuro
            atr_multiplier=row["atr_multiplier"],
            trailing_mode="percent",
            trailing_value=row["trailing_value"],
        )
        self.profile_engine.add_profile(profile)
        return profile
