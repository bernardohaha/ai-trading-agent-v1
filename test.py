from data_collector import DataCollector
from technical_analysis import TechnicalAnalyzer
from support_resistance_engine import SupportResistanceEngine
from decision_engine import DecisionEngine
from alert_system import AlertSystem
from paper_trader import PaperTrader
from scoring_engine import ScoringEngine

# Recolha de dados
collector = DataCollector()
ohlcv = collector.get_historical_ohlcv(
    symbol="BTCUSDT", interval="1h", lookback="3 months ago UTC"
)

# Indicadores Técnicos
analyzer = TechnicalAnalyzer(ohlcv)
ohlcv = analyzer.calculate_indicators()

# Suportes e Resistências
sr_engine = SupportResistanceEngine(ohlcv)
levels = sr_engine.clusterize_levels()
current_price = ohlcv["close"].iloc[-1]
closest_support, closest_resistance = sr_engine.classify_levels(current_price, levels)
zone, support, resistance = sr_engine.suggest_trade_zone(
    current_price, closest_support, closest_resistance
)

# Decisão básica
decision_engine = DecisionEngine()
decision = decision_engine.make_decision(zone, support, resistance, current_price)

# Alerta
alert_system = AlertSystem()
alert_system.send_alert(
    "Novo sinal gerado!", zone, decision, support, resistance, current_price
)

# Paper Trading
trader = PaperTrader()
trader.execute_trade(decision, current_price)

# Estado do Paper Trader
status = trader.get_status()
print("=== PAPER TRADER STATUS ===")
for key, value in status.items():
    print(f"{key}: {value}")

# Fibonacci Levels
fib_levels = analyzer.calculate_fibonacci_levels()

print("\n=== Fibonacci Levels ===")
for level, price in fib_levels.items():
    print(f"{level}: {price:.2f}")

# MACD, RSI, ATR (último valor)
last_macd = ohlcv["macd"].iloc[-1]
last_rsi = ohlcv["rsi"].iloc[-1]
last_atr = ohlcv["atr"].iloc[-1]

print("\n=== Other Indicators ===")
print(f"MACD: {last_macd:.4f}")
print(f"RSI: {last_rsi:.2f}")
print(f"ATR: {last_atr:.2f}")

# Scoring Engine
scoring_engine = ScoringEngine()
score = scoring_engine.calculate_score(ohlcv, fib_levels, zone, current_price)

print(f"\n=== SCORING SYSTEM ===")
print(f"AI Technical Score: {score}/4")

if score >= 3:
    print("✅ CONDIÇÃO DE ENTRADA CONFIRMADA")
else:
    print("❌ CONDIÇÃO DE ENTRADA INSUFICIENTE")
