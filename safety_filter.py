class SafetyFilter:
    def __init__(self, config):
        self.max_rsi = config["max_rsi"]
        self.min_rsi = config["min_rsi"]
        self.max_atr = config["max_atr"]
        self.macd_min = config["macd_min"]

    def check_safety(self, ohlcv):
        rsi = ohlcv["rsi"].iloc[-1]
        atr = ohlcv["atr"].iloc[-1]
        macd = ohlcv["macd"].iloc[-1]

        reasons = []

        if rsi > self.max_rsi:
            reasons.append("RSI extremamente elevado")
        if rsi < self.min_rsi:
            reasons.append("RSI extremamente baixo")
        if atr > self.max_atr:
            reasons.append("Volatilidade excessiva (ATR)")
        if macd < self.macd_min:
            reasons.append("Momentum negativo extremo (MACD)")

        if reasons:
            return False, reasons
        else:
            return True, ["Safe"]
