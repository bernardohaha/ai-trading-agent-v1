from data_collector import DataCollector
from technical_analysis import TechnicalAnalyzer
from support_resistance_engine import SupportResistanceEngine
from renko_engine import RenkoEngine
from decision_engine import DecisionEngine
from safety_filter import SafetyFilter
from alert_system import AlertSystem
from paper_trader import PaperTrader
from scoring_engine import ScoringEngine
from performance_tracker import PerformanceTracker

# Recolha de dados
collector = DataCollector()
ohlcv = collector.get_historical_ohlcv(
    symbol="BTCUSDT", interval="1h", lookback="6 months ago UTC"
)

# Inicialização de todos os módulos
decision_engine = DecisionEngine()
alert_system = AlertSystem()
trader = PaperTrader()
scoring_engine = ScoringEngine()
safety_filter = SafetyFilter()
performance = PerformanceTracker()

# Ciclo contínuo otimizado (mini-backtest controlado)
for i in range(150, len(ohlcv)):  # Delay inicial maior para garantir dados suficientes
    ohlcv_slice = ohlcv.iloc[:i].copy()

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

    renko_engine = RenkoEngine(ohlcv_slice)
    renko_series = renko_engine.build_renko()
    renko_trend = renko_engine.detect_trend(renko_series)

    score = scoring_engine.calculate_score(
        ohlcv_slice, fib_levels, zone, renko_trend, current_price
    )

    safety_pass, reasons = safety_filter.check_safety(ohlcv_slice)

    if score >= 4 and safety_pass:
        decision = decision_engine.make_decision(
            zone, support, resistance, current_price
        )
        alert_system.send_alert(
            "Novo sinal gerado!", zone, decision, support, resistance, current_price
        )
        pnl = trader.execute_trade(decision, current_price)
        if pnl is not None:
            performance.log_trade(pnl)

# Output final de performance
print("\n=== FINAL PERFORMANCE REPORT ===")
report = performance.get_report()
for key, value in report.items():
    print(f"{key}: {value}")
