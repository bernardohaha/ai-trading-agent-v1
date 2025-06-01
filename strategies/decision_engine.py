class DecisionEngine:
    def __init__(self, position=None):
        self.position = position  # Pode ser 'LONG', 'SHORT' ou None

    def make_decision(self, zone, support, resistance, current_price):
        decision = "HOLD"

        if self.position is None:
            if zone == "BUY ZONE":
                decision = "ENTER LONG"
                self.position = "LONG"
            elif zone == "SELL ZONE":
                decision = "ENTER SHORT"
                self.position = "SHORT"

        elif self.position == "LONG":
            if resistance and current_price >= resistance * 0.99:
                decision = "EXIT LONG"
                self.position = None

        elif self.position == "SHORT":
            if support and current_price <= support * 1.01:
                decision = "EXIT SHORT"
                self.position = None

        return decision
