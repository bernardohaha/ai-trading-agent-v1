from ai_trading_agent.core.profile_engine import ProfileConfig


def load_profiles():
    scalping = ProfileConfig(
        name="Scalping",
        risk_per_trade=0.01,  # 1%
        max_daily_loss=0.05,  # 5%
        atr_multiplier=1.5,
        trailing_mode="percent",
        trailing_value=0.3,  # 0.3% trailing stop
    )

    swing = ProfileConfig(
        name="Swing",
        risk_per_trade=0.02,
        max_daily_loss=0.05,
        atr_multiplier=2.0,
        trailing_mode="percent",
        trailing_value=1.0,
    )

    momentum = ProfileConfig(
        name="Momentum",
        risk_per_trade=0.015,
        max_daily_loss=0.04,
        atr_multiplier=1.8,
        trailing_mode="percent",
        trailing_value=0.5,
    )

    return [scalping, swing, momentum]
