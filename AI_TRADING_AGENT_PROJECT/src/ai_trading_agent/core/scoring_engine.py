class ScoringEngine:
    def __init__(self, config):
        self.weights = {
            "renko_trend": config["renko_weight"],
            "fib_zone_alignment": config["fib_weight"],
            "rsi_score": config["rsi_weight"],
            "support_resistance_proximity": config["sr_weight"],
            "macd_signal": config["macd_weight"],
            "ema_score": config["ema_weight"],  # Novo
            "volume_score": config["volume_weight"],  # Novo
        }
        self.threshold = config["threshold"]

    def calculate_score(self, ohlcv, fib_levels, zone, renko_trend, current_price):
        score = 0

        # Renko
        if renko_trend == "UP":
            score += self.weights["renko_trend"]

        # Fibo Alignment
        fib_score = self._fib_score(current_price, fib_levels)
        score += fib_score * self.weights["fib_zone_alignment"]

        # RSI
        rsi = ohlcv["rsi"].iloc[-1]
        if 40 <= rsi <= 60:
            score += self.weights["rsi_score"]

        # Support/Resistance zone
        if zone == "BUY ZONE":
            score += self.weights["support_resistance_proximity"]

        # MACD
        macd = ohlcv["macd"].iloc[-1]
        if macd > 0:
            score += self.weights["macd_signal"]

        # EMA
        ema_fast = ohlcv["ema_fast"].iloc[-1]
        ema_slow = ohlcv["ema_slow"].iloc[-1]
        ema_score = self.score_ema(ema_fast, ema_slow)
        score += ema_score * self.weights["ema_score"]

        # Volume
        current_volume = ohlcv["volume"].iloc[-1]
        average_volume = ohlcv["volume"].rolling(window=20).mean().iloc[-1]
        volume_score = self.score_volume(current_volume, average_volume)
        score += volume_score * self.weights["volume_score"]

        # Retornar um objeto IndicatorScores com os scores individuais
        from ai_trading_agent.core.decision_engine import IndicatorScores

        return IndicatorScores(
            rsi=ohlcv["rsi"].iloc[-1],
            ema_signal=ema_score,
            macd_signal=ohlcv["macd"].iloc[-1],
            volume_signal=volume_score,
            support_resistance_signal=1
            if zone == "BUY ZONE"
            else 0,  # Simplificado para este exemplo
        )

    def _fib_score(self, price, fib_levels):
        if fib_levels["38.2%"] <= price <= fib_levels["61.8%"]:
            return 1
        else:
            return 0

    def score_ema(self, ema_fast, ema_slow):
        if ema_fast > ema_slow:
            return 1  # Bullish crossover
        elif ema_fast < ema_slow:
            return -1  # Bearish crossover
        else:
            return 0

    def score_volume(self, current_volume, average_volume):
        if current_volume > average_volume * 1.5:
            return 1  # Volume spike
        elif current_volume < average_volume * 0.5:
            return -1  # Low volume
        else:
            return 0
