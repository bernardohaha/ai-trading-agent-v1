from binance import Client
import pandas as pd
import datetime


class DataCollector:
    def __init__(self):
        self.client = Client()

    def get_historical_ohlcv(
        self, symbol: str, interval: str, lookback: str = "1 month ago UTC"
    ):
        klines = self.client.get_historical_klines(symbol, interval, lookback)

        ohlcv = pd.DataFrame(
            klines,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "number_of_trades",
                "taker_buy_base_volume",
                "taker_buy_quote_volume",
                "ignore",
            ],
        )

        ohlcv["open_time"] = pd.to_datetime(ohlcv["open_time"], unit="ms")
        ohlcv.set_index("open_time", inplace=True)
        numeric_columns = ["open", "high", "low", "close", "volume"]
        ohlcv[numeric_columns] = ohlcv[numeric_columns].astype(float)

        return ohlcv
