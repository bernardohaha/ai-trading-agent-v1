import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
from binance_client import BinanceClient
from technical_analysis import TechnicalAnalyzer
from support_resistance_engine import SupportResistanceEngine
from renko_engine import RenkoEngine
from decision_engine import DecisionEngine
from safety_filter import SafetyFilter
from alert_system import AlertSystem
from paper_trader import PaperTrader
from scoring_engine import ScoringEngine
from performance_tracker import PerformanceTracker
from position_manager import PositionManager
from status_logger import StatusLogger
from circuit_breaker import CircuitBreaker
from data_validator import DataValidator
from configloader import ConfigLoader

# Load Config
config_loader = ConfigLoader()
scoring_config = config_loader.get_scoring_config()
pm_config = config_loader.get_position_manager_config()
sf_config = config_loader.get_safety_filter_config()
cb_config = config_loader.get_circuit_breaker_config()

# Configurações gerais
SYMBOL = "BTCUSDT"
INTERVAL = "5m"
LOOKBACK_CANDLES = 150
REFRESH_SECONDS = 30

# Inicializações dos módulos
binance = BinanceClient()
decision_engine = DecisionEngine()
alert_system = AlertSystem()  # ATUALIZADO - agora já com Telegram
trader = PaperTrader()
scoring_engine = ScoringEngine(scoring_config)
safety_filter = SafetyFilter(sf_config)
performance = PerformanceTracker()
status_logger = StatusLogger()
circuit_breaker = CircuitBreaker(cb_config)
validator = DataValidator()

position_manager = None

print("AI Agent Live Mode iniciado...")

while True:
    try:
        cb_ok, cb_msg = circuit_breaker.check()
        if not cb_ok:
            print(f"[Circuit Breaker Ativado] {cb_msg}")
            time.sleep(REFRESH_SECONDS)
            continue

        ohlcv = binance.get_historical_ohlcv(
            symbol=SYMBOL, interval=INTERVAL, limit=LOOKBACK_CANDLES
        )

        valid, validation_msg = validator.validate(ohlcv)
        if not valid:
            print(f"[VALIDAÇÃO FALHOU] {validation_msg}")
            time.sleep(REFRESH_SECONDS)
            continue

        analyzer = TechnicalAnalyzer(ohlcv)
        ohlcv = analyzer.calculate_indicators()
        fib_levels = analyzer.calculate_fibonacci_levels()

        sr_engine = SupportResistanceEngine(ohlcv)
        levels = sr_engine.clusterize_levels()
        current_price = ohlcv["close"].iloc[-1]
        closest_support, closest_resistance = sr_engine.classify_levels(
            current_price, levels
        )
        zone, support, resistance = sr_engine.suggest_trade_zone(
            current_price, closest_support, closest_resistance
        )

        renko_engine = RenkoEngine(ohlcv)
        renko_series = renko_engine.build_renko()
        renko_trend = renko_engine.detect_trend(renko_series)

        score = scoring_engine.calculate_score(
            ohlcv, fib_levels, zone, renko_trend, current_price
        )
        safety_pass, reasons = safety_filter.check_safety(ohlcv)

        if trader.position == "NONE":
            if score >= scoring_engine.threshold and safety_pass:
                decision = "ENTER LONG"
                alert_system.send_alert(
                    "Novo sinal gerado!",
                    zone,
                    decision,
                    support,
                    resistance,
                    current_price,
                )
                pnl = trader.execute_trade(decision, current_price)
                if pnl is not None:
                    performance.log_trade(pnl)
                    performance.save_performance()
                position_manager = PositionManager(
                    entry_price=current_price, config=pm_config
                )

        else:
            if position_manager:
                action = position_manager.update(current_price)

                if action in ["EXIT TAKE PROFIT", "EXIT STOP LOSS", "CHECK FOR EXIT"]:
                    decision = "EXIT LONG"
                    alert_system.send_alert(
                        f"{action}", zone, decision, support, resistance, current_price
                    )
                    pnl = trader.execute_trade(decision, current_price)
                    if pnl is not None:
                        performance.log_trade(pnl)
                        performance.save_performance()
                    position_manager = None

        floating_pnl = 0
        if trader.position == "LONG":
            floating_pnl = round((current_price - trader.entry_price), 2)
        status_logger.update_status(
            position=trader.position,
            entry_price=trader.entry_price,
            pnl=floating_pnl,
            position_action="ACTIVE" if position_manager else "WAITING",
        )

        report = performance.get_report()
        print("\n[Live Performance]")
        for key, value in report.items():
            print(f"{key}: {value}")

        time.sleep(REFRESH_SECONDS)

    except KeyboardInterrupt:
        print("\nLive agent parado manualmente.")
        break

    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(10)
