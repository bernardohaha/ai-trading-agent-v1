class SafetyFilter:
    def __init__(self):
        pass

    def check_safety(self, ohlcv):
        rsi = ohlcv["rsi"].iloc[-1]
        atr = ohlcv["atr"].iloc[-1]
        macd = ohlcv["macd"].iloc[-1]

        reasons = []

        if rsi > 75:
            reasons.append("RSI extremamente elevado")
        if rsi < 20:
            reasons.append("RSI extremamente baixo")
        if atr > 1000:
            reasons.append("Volatilidade excessiva")
        if macd < -100:
            reasons.append("Momentum negativo extremo")

        if reasons:
            return False, reasons
        else:
            return True, ["Safe"]
