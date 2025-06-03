import logging
from ai_trading_agent.core.profile_engine import ProfileEngine, ProfileConfig
from ai_trading_agent.core.risk_manager import RiskManager
from ai_trading_agent.core.position_sizer import PositionSizer
from ai_trading_agent.core.trailing_stop import TrailingStop
from ai_trading_agent.core.technical_analysis import TechnicalAnalyzer
from ai_trading_agent.core.scoring_engine import ScoringEngine


class Orchestrator:
    def __init__(
        self,
        account_balance,
        profile_engine: ProfileEngine,
        active_profile_name: str,
        scoring_config: dict,
    ):
        self.account_balance = account_balance
        self.profile_engine = profile_engine
        self.profile_engine.set_active_profile(active_profile_name)
        self.profile = self.profile_engine.get_active_config()

        if self.profile is None:
            raise ValueError(
                f"Profile '{active_profile_name}' not found in ProfileEngine."
            )

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

        self.scoring_engine = ScoringEngine(scoring_config)

        logging.basicConfig(level=logging.INFO)

    def evaluate_trade(self, entry_price, stop_loss_price, atr_value, highest_price):
        if not self.risk_manager.can_open_trade(entry_price, stop_loss_price):
            logging.warning("Trade não aprovado pelo Risk Manager.")
            return None

        position_size = self.position_sizer.calculate_size(atr_value, entry_price)
        return position_size

    def run_full_scoring(self, ohlcv, fib_levels, zone, renko_trend, current_price):
        score = self.scoring_engine.calculate_score(
            ohlcv, fib_levels, zone, renko_trend, current_price
        )
        logging.info(f"Score total: {score}")
        return score
