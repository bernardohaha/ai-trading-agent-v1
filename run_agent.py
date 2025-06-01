from data_collector import DataCollector
from technical_analysis import TechnicalAnalyzer
from support_resistance_engine import SupportResistanceEngine
from decision_engine import DecisionEngine
from alert_system import AlertSystem
from paper_trader import PaperTrader
from scoring_engine import ScoringEngine

# Recolher dados históricos
collector = DataCollector()
ohlcv = collector.get_historical_ohlcv(
    symbol="BTCUSDT", interval="1h", lookback="6 months ago UTC"
)

# Inicializar módulos
decision_engine = DecisionEngine()
alert_system = AlertSystem()
trader = PaperTrader()
scoring_engine = ScoringEngine()

# Loop contínuo sobre cada candle (mini backtest)
for i in range(
    100, len(ohlcv)
):  # começamos em 50 para garantir dados suficientes para os indicadores
    ohlcv_slice = ohlcv.iloc[:i].copy()  # usar apenas dados até este candle
    analyzer = TechnicalAnalyzer(ohlcv_slice)
    ohlcv_slice = analyzer.calculate_indicators()
    fib_levels = analyzer.calculate_fibonacci_levels()

    sr_engine = SupportResistanceEngine(ohlcv_slice)
    levels = sr_engine.clusterize_levels()
    current_price = ohlcv_slice["close"].iloc[-1]
    closest_support, closest_resistance = sr_engine.classify_levels(
        current_price, levels
    )
    zone, support, resistance = sr_engine.suggest_trade_zone(
        current_price, closest_support, closest_resistance
    )

    score = scoring_engine.calculate_score(ohlcv_slice, fib_levels, zone, current_price)

    if score >= 3:
        decision = decision_engine.make_decision(
            zone, support, resistance, current_price
        )
        alert_system.send_alert(
            "Novo sinal gerado!", zone, decision, support, resistance, current_price
        )
        trader.execute_trade(decision, current_price)

# No fim do ciclo mostrar resultados
print("\n=== FINAL REPORT ===")
status = trader.get_status()
for key, value in status.items():
    print(f"{key}: {value}")
