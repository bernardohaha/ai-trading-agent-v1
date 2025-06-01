class ScoringEngine:
    def __init__(self, config):
        self.weights = {
            "renko_trend": config["renko_weight"],
            "fib_zone_alignment": config["fib_weight"],
            "rsi_score": config["rsi_weight"],
            "support_resistance_proximity": config["sr_weight"],
            "macd_signal": config["macd_weight"],
        }
        self.threshold = config["threshold"]

    def calculate_score(self, ohlcv, fib_levels, zone, renko_trend, current_price):
        score = 0

        if renko_trend == "UP":
            score += self.weights["renko_trend"]

        fib_score = self._fib_score(current_price, fib_levels)
        score += fib_score * self.weights["fib_zone_alignment"]

        rsi = ohlcv["rsi"].iloc[-1]
        if 40 <= rsi <= 60:
            score += self.weights["rsi_score"]

        if zone == "BUY ZONE":
            score += self.weights["support_resistance_proximity"]

        macd = ohlcv["macd"].iloc[-1]
        if macd > 0:
            score += self.weights["macd_signal"]

        return round(score, 2)

    def _fib_score(self, price, fib_levels):
        if fib_levels["38.2%"] <= price <= fib_levels["61.8%"]:
            return 1
        else:
            return 0
