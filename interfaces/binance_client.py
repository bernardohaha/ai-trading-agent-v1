import os
from dotenv import load_dotenv
from binance.client import Client

# Carregar as chaves do ficheiro .env
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
TESTNET = os.getenv("BINANCE_TESTNET") == "True"


class BinanceClient:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET)
        if TESTNET:
            self.client.API_URL = "https://testnet.binance.vision/api"

    def get_historical_ohlcv(self, symbol, interval, limit=500):
        data = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        ohlcv = {
            "open_time": [],
            "open": [],
            "high": [],
            "low": [],
            "close": [],
            "volume": [],
        }
        for candle in data:
            ohlcv["open_time"].append(candle[0])
            ohlcv["open"].append(float(candle[1]))
            ohlcv["high"].append(float(candle[2]))
            ohlcv["low"].append(float(candle[3]))
            ohlcv["close"].append(float(candle[4]))
            ohlcv["volume"].append(float(candle[5]))
        import pandas as pd

        df = pd.DataFrame(ohlcv)
        return df
