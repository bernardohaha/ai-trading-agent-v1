# orchestrator.py

from profile_engine import ProfileEngine, ProfileConfig
from risk_manager import RiskManager
from position_sizer import PositionSizer
from trailing_stop import TrailingStop

import logging


class Orchestrator:
    def __init__(
        self, account_balance, profile_engine: ProfileEngine, active_profile_name: str
    ):
        self.account_balance = account_balance
        self.profile_engine = profile_engine
        self.profile_engine.set_active_profile(active_profile_name)
        self.profile = self.profile_engine.get_active_config()

        self.risk_manager = RiskManager(
            account_balance=self.account_balance,
            risk_per_trade=self.profile["risk_per_trade"],
            max_daily_loss=self.profile["max_daily_loss"],
        )

        self.position_sizer = PositionSizer(
            account_balance=self.account_balance,
            risk_per_trade=self.profile["risk_per_trade"],
            atr_multiplier=self.profile["atr_multiplier"],
        )

        self.trailing_stop = TrailingStop(
            mode=self.profile["trailing_mode"],
            trailing_value=self.profile["trailing_value"],
        )

        logging.basicConfig(level=logging.INFO)

    def evaluate_trade(self, entry_price, stop_loss_price, atr_value, highest_price):
        """
        Fluxo completo para avaliar a operação.
        """

        if not self.risk_manager.can_open_trade(entry_price, stop_loss_price):
            logging.warning("Trade não aprovado pelo Risk Manager.")
            return None

        position_size = self.position_sizer.calculate_size(atr_value, entry_price)

        trailing_price = self.trailing_stop.calculate_stop(entry_price, highest_price)

        return {"position_size": position_size, "trailing_stop": trailing_price}
