import numpy as np


class DataValidator:
    def __init__(self, max_price_jump_pct=0.10):
        self.max_price_jump_pct = max_price_jump_pct

    def validate(self, ohlcv):
        # Verifica se o dataframe está vazio
        if ohlcv is None or ohlcv.empty:
            return False, "OHLCV vazio"

        # Verifica por valores NaN
        if ohlcv.isnull().values.any():
            return False, "OHLCV com NaNs detectados"

        # Verifica saltos de preço extremos
        price_change = ohlcv["close"].pct_change()
        if price_change.abs().iloc[-1] > self.max_price_jump_pct:
            return (
                False,
                f"Salto de preço suspeito detectado: {price_change.iloc[-1] * 100:.2f}%",
            )

        return True, "OK"
