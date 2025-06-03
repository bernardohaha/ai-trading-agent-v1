import pandas as pd
import ta


class TechnicalAnalyzer:
    def __init__(self, ohlcv: pd.DataFrame):
        self.ohlcv = ohlcv

    def calculate_indicators(self):
        # EMA (ajustável via config externa — para já hardcoded)
        self.ohlcv["ema_fast"] = ta.trend.ema_indicator(self.ohlcv["close"], window=50)
        self.ohlcv["ema_slow"] = ta.trend.ema_indicator(self.ohlcv["close"], window=200)

        # RSI
        self.ohlcv["rsi"] = ta.momentum.rsi(self.ohlcv["close"], window=14)

        # MACD (usamos o macd_diff simplificado)
        self.ohlcv["macd"] = ta.trend.macd_diff(self.ohlcv["close"])

        # ATR (exemplo para futura gestão de risco)
        self.ohlcv["atr"] = ta.volatility.average_true_range(
            self.ohlcv["high"], self.ohlcv["low"], self.ohlcv["close"], window=14
        )

        return self.ohlcv

    def calculate_fibonacci_levels(self):
        max_price = self.ohlcv["high"].max()
        min_price = self.ohlcv["low"].min()

        diff = max_price - min_price

        levels = {
            "0.0%": max_price,
            "23.6%": max_price - 0.236 * diff,
            "38.2%": max_price - 0.382 * diff,
            "50.0%": max_price - 0.5 * diff,
            "61.8%": max_price - 0.618 * diff,
            "78.6%": max_price - 0.786 * diff,
            "100%": min_price,
        }

        return levels
