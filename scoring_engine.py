class ScoringEngine:
    def __init__(self):
        pass

    def calculate_score(self, ohlcv, fib_levels, zone, renko_trend, current_price):
        score = 0

        # RSI
        rsi = ohlcv["rsi"].iloc[-1]
        if rsi < 40:
            score += 1

        # MACD
        macd = ohlcv["macd"].iloc[-1]
        if macd > 0:
            score += 1

        # Fibonacci (se o preço está próximo de níveis relevantes)
        for key, level in fib_levels.items():
            if (
                key in ["38.2%", "50.0%"]
                and abs(current_price - level) / current_price < 0.02
            ):
                score += 1
                break

        # Zona do suporte/resistência
        if zone == "BUY ZONE":
            score += 1

        # Renko Trend
        if renko_trend == "UP":
            score += 1

        return score
