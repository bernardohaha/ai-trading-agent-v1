from ai_trading_agent.core.binance_client import BinanceClient
import pandas as pd
import datetime


class DataCollector:
    def __init__(self):
        self.client = BinanceClient()

    def get_historical_ohlcv(self, symbol: str, interval: str, limit: int = 1000):
        ohlcv_data = self.client.get_historical_ohlcv(symbol, interval, limit)

        ohlcv = pd.DataFrame(
            ohlcv_data,
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
