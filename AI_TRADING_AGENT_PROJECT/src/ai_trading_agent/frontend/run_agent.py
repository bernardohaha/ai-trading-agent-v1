import asyncio
import logging
from ai_trading_agent.core.data_collector import DataCollector
from ai_trading_agent.core.technical_analysis import TechnicalAnalyzer
from ai_trading_agent.core.support_resistance_engine import (
    SupportResistanceEngine,
)
from ai_trading_agent.core.renko_engine import RenkoEngine
from ai_trading_agent.core.safety_filter import SafetyFilter
from ai_trading_agent.core.interfaces.alert_system import AlertSystem
from ai_trading_agent.core.paper_trader import PaperTrader
from ai_trading_agent.core.performance_tracker import PerformanceTracker
from ai_trading_agent.core.configloader import ConfigLoader
from ai_trading_agent.config.profiles_config import load_profiles
from ai_trading_agent.core.profile_engine import ProfileEngine
from ai_trading_agent.core.orchestrator import Orchestrator
from ai_trading_agent.core.decision_engine import DecisionEngine

logging.basicConfig(level=logging.INFO)


async def main():
    # Carregar configuração geral e scoring
    config_loader = ConfigLoader(file_path="ai_trading_agent/data/config.yaml")
    config = config_loader.config
    scoring_config = config_loader.get_scoring_config()

    # Carregar perfis e ativar profile engine
    profiles = load_profiles()
    profile_engine = ProfileEngine()
    for p in profiles:
        profile_engine.add_profile(p)

    # Instanciar o Orchestrator com o profile ativo e configs
    orchestrator = Orchestrator(
        account_balance=10000,
        profile_engine=profile_engine,
        active_profile_name="Scalping",
        scoring_config=scoring_config,
    )

    # Instanciar o DecisionEngine diretamente no run_agent
    decision_engine = DecisionEngine()

    # Restantes módulos auxiliares
    safety_filter = SafetyFilter(config=config_loader.get_safety_filter_config())
    trader = PaperTrader()
    alert_system = AlertSystem()
    performance = PerformanceTracker()

    # Recolha de dados
    collector = DataCollector()
    ohlcv = collector.get_historical_ohlcv(symbol="BTCUSDT", interval="1h", limit=500)

    # Loop contínuo
    for i in range(150, len(ohlcv)):
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

        # Safety Filter (mantemos)
        safety_pass, reasons = safety_filter.check_safety(ohlcv_slice)

        if safety_pass:
            # Sincronizar o estado do trader no DecisionEngine
            decision_engine.position = trader.position

            # Análise completa via Orchestrator
            indicator_scores = orchestrator.run_full_scoring(
                ohlcv_slice, fib_levels, zone, renko_trend, current_price
            )

            decision = decision_engine.make_decision(indicator_scores)

            # Executa o trade
            pnl = trader.execute_trade(decision, current_price)
            if pnl is not None:
                performance.log_trade(pnl)

            # Apenas envia alertas nas entradas
            if decision in ["ENTER LONG", "ENTER SHORT"]:
                await alert_system.send_alert(
                    "Novo sinal gerado!",
                    zone,
                    decision,
                    support,
                    resistance,
                    current_price,
                )

    # Output final de performance
    print("\n=== FINAL PERFORMANCE REPORT ===")
    report = performance.get_report()
    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
