class IndicatorScores:
    def __init__(
        self, rsi, ema_signal, macd_signal, volume_signal, support_resistance_signal
    ):
        self.rsi = rsi
        self.ema_signal = ema_signal
        self.macd_signal = macd_signal
        self.volume_signal = volume_signal
        self.support_resistance_signal = support_resistance_signal

    def total_score(self):
        return (
            self.rsi
            + self.ema_signal
            + self.macd_signal
            + self.volume_signal
            + self.support_resistance_signal
        )


class DecisionEngine:
    def __init__(self, position=None):
        self.position = position  # Pode ser 'LONG', 'SHORT' ou None

    def make_decision(self, indicator_scores: IndicatorScores):
        decision = "HOLD"
        total = indicator_scores.total_score()

        # Entradas (mantemos iguais)
        if total >= 3:
            decision = "ENTER LONG"
            self.position = "LONG"

        elif total <= -3:
            decision = "ENTER SHORT"
            self.position = "SHORT"

        # Exits - agora com thresholds hiper flexíveis só para debug
        elif self.position == "LONG" and total < 1:
            decision = "EXIT LONG"
            self.position = None

        elif self.position == "SHORT" and total > -1:
            decision = "EXIT SHORT"
            self.position = None

        return decision
