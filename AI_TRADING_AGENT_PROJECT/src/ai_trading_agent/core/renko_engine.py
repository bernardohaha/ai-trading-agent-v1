import numpy as np
import pandas as pd


class RenkoEngine:
    def __init__(self, ohlcv, brick_size=None):
        self.ohlcv = ohlcv
        self.brick_size = brick_size or self.calculate_brick_size()

    def calculate_brick_size(self):
        atr = self.ohlcv["close"].rolling(window=14).apply(lambda x: np.ptp(x)).mean()
        return atr * 0.5  # Podes ajustar este fator para mais ou menos sensibilidade

    def build_renko(self):
        prices = self.ohlcv["close"].values
        renko = [prices[0]]

        for price in prices[1:]:
            move = price - renko[-1]

            if abs(move) >= self.brick_size:
                bricks = int(move / self.brick_size)
                for _ in range(abs(bricks)):
                    renko.append(renko[-1] + self.brick_size * np.sign(bricks))

        renko_series = pd.Series(renko, index=self.ohlcv.index[: len(renko)])
        return renko_series

    def detect_trend(self, renko_series):
        diffs = renko_series.diff().dropna()
        up_moves = diffs[diffs > 0].count()
        down_moves = diffs[diffs < 0].count()

        if up_moves > down_moves:
            return "UP"
        elif down_moves > up_moves:
            return "DOWN"
        else:
            return "SIDEWAYS"
