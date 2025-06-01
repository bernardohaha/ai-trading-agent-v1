class PaperTrader:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.position = None
        self.entry_price = None
        self.trade_log = []

    def execute_trade(self, decision, current_price):
        if decision == "ENTER LONG" and self.position is None:
            self.position = "LONG"
            self.entry_price = current_price
            print(f"🟢 OPEN LONG at {current_price:.2f}")

        elif decision == "EXIT LONG" and self.position == "LONG":
            profit = current_price - self.entry_price
            self.balance += profit
            print(f"🔴 CLOSE LONG at {current_price:.2f} | PnL: {profit:.2f}")
            self.trade_log.append(profit)
            self.position = None
            self.entry_price = None

        # Podemos mais tarde adicionar lógica de short
        # elif decision == "ENTER SHORT" ...

    def get_status(self):
        return {
            "balance": self.balance,
            "position": self.position,
            "entry_price": self.entry_price,
            "trades": len(self.trade_log),
            "total_pnl": sum(self.trade_log),
            "average_pnl": sum(self.trade_log) / len(self.trade_log)
            if self.trade_log
            else 0,
        }
