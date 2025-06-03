import sys
import os
import asyncio  # Importar asyncio


import time
from ai_trading_agent.core.interfaces.binance_client import BinanceClient
from ai_trading_agent.core.technical_analysis import TechnicalAnalyzer
from ai_trading_agent.core.support_resistance_engine import (
    SupportResistanceEngine,
)
from ai_trading_agent.core.renko_engine import RenkoEngine
from ai_trading_agent.core.decision_engine import DecisionEngine
from ai_trading_agent.core.safety_filter import SafetyFilter
from ai_trading_agent.core.interfaces.alert_system import AlertSystem
from ai_trading_agent.core.paper_trader import PaperTrader
from ai_trading_agent.core.scoring_engine import ScoringEngine
from ai_trading_agent.core.performance_tracker import PerformanceTracker
from ai_trading_agent.core.position_manager import PositionManager
from ai_trading_agent.core.status_logger import StatusLogger
from ai_trading_agent.core.circuit_breaker_engine import CircuitBreakerEngine
from ai_trading_agent.core.configloader import ConfigLoader
from ai_trading_agent.core.data_validator import DataValidator
from ai_trading_agent.core.interfaces.telegram_alerts import TelegramAlerts


async def main():  # Definir função assíncrona principal
    # Load Config
    config_loader = ConfigLoader(
        file_path="ai_trading_agent/data/config.yaml"
    )  # Passar o caminho correto
    scoring_config = config_loader.get_scoring_config()
    pm_config = config_loader.get_position_manager_config()
    sf_config = config_loader.get_safety_filter_config()
    cb_config = config_loader.get_circuit_breaker_config()

    # Configurações gerais
    SYMBOL = "BTCUSDT"
    INTERVAL = "5m"
    LOOKBACK_CANDLES = 150
    REFRESH_SECONDS = 30

    # Inicializações
    binance = BinanceClient()
    decision_engine = DecisionEngine()
    alert_system = AlertSystem()
    telegram = TelegramAlerts()
    trader = PaperTrader()
    trader.position = "NONE"  # Garantir que o agente começa sem posição aberta
    scoring_engine = ScoringEngine(config=scoring_config)
    safety_filter = SafetyFilter(config=sf_config)
    performance = PerformanceTracker()
    validator = DataValidator()
    position_manager = None
    status_logger = StatusLogger()

    # Novo: Circuit Breaker
    circuit_breaker = CircuitBreakerEngine(
        max_daily_loss_pct=cb_config.get("max_daily_loss_pct", 0.05),
        max_consecutive_losses=cb_config.get("max_consecutive_losses", 5),
    )

    print("AI Agent Live Mode iniciado...")

    while True:
        try:
            action = "WAITING"  # Inicializar action com valor padrão no início do loop
            trader.position = "NONE"  # Garantir que a posição é NONE no início de cada iteração (para contornar o erro)

            # Validar se o Circuit Breaker bloqueou
            halted, reason = circuit_breaker.should_halt_trading(trader.balance)
            if halted:
                print(reason)
                await telegram.send_message(f"🚨 Circuit Breaker Ativado!\n{reason}")
                status_logger.update({"manager_state": "HALTED"})
                await asyncio.sleep(REFRESH_SECONDS)
                continue

            # Coleta de dados
            ohlcv = binance.get_historical_ohlcv(
                symbol=SYMBOL, interval=INTERVAL, limit=LOOKBACK_CANDLES
            )
            validator.validate(ohlcv)

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

            # DECISÃO
            if trader.position == "NONE":
                if score >= scoring_config.get("entry_threshold", 4) and safety_pass:
                    decision = "ENTER LONG"
                    await alert_system.send_alert(
                        "Novo sinal gerado!",
                        zone,
                        decision,
                        support,
                        resistance,
                        current_price,
                    )
                    await telegram.send_message(
                        f"📊 Nova entrada: {SYMBOL} a {current_price}"
                    )
                    pnl = trader.execute_trade(decision, current_price)
                    if pnl is not None:
                        performance.log_trade(pnl)
                        performance.save_performance()
                    position_manager = PositionManager(
                        entry_price=current_price, config=pm_config
                    )
            else:  # Se trader.position não for "NONE"
                action = "WAITING"  # Inicializar action com valor padrão
                if position_manager:  # Verificar se position_manager foi inicializado
                    action = position_manager.update(current_price)

                    if action in [
                        "EXIT TAKE PROFIT",
                        "EXIT STOP LOSS",
                        "CHECK FOR EXIT",
                    ]:
                        decision = "EXIT LONG"
                        await alert_system.send_alert(
                            f"{action}",
                            zone,
                            decision,
                            support,
                            resistance,
                            current_price,
                        )
                        await telegram.send_message(
                            f"📉 Fecho posição: {SYMBOL} a {current_price}"
                        )
                        pnl = trader.execute_trade(decision, current_price)
                        if pnl is not None:
                            performance.log_trade(pnl)
                            performance.save_performance()
                            circuit_breaker.update_daily(pnl)
                        position_manager = (
                            None  # Resetar position_manager após fechar a posição
                        )
                    # Se a ação for "HOLD", a variável action já tem o valor retornado por position_manager.update
                else:  # Se position_manager for None mas trader.position não for "NONE", estado inconsistente
                    print(
                        "[Live Agent Error]: position_manager is None but trader.position is not 'NONE'. Cannot manage existing position without PositionManager."
                    )
                    # Continuar o ciclo, mas sem gerir a posição existente
                    action = "ERROR - No Manager"  # Atribuir um estado de erro para o logging

            # Estado parcial (visível)
            report = performance.get_report()
            print("\n[Live Performance]")
            for key, value in report.items():
                print(f"{key}: {value}")

            # Calcular PnL flutuante se a posição estiver aberta
            floating_pnl_value = 0
            if trader.position != "NONE" and trader.entry_price is not None:
                floating_pnl_value = current_price - trader.entry_price

            # Logging
            status_logger.update(
                {
                    "position": trader.position,
                    "entry_price": trader.entry_price,
                    "floating_pnl": floating_pnl_value,
                    "manager_state": action,  # Usar a variável action
                }
            )

            await asyncio.sleep(REFRESH_SECONDS)

        except KeyboardInterrupt:
            print("\nLive agent parado manualmente.")
            break

        except Exception as e:
            print(f"Erro: {e}")
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())  # Executar a função assíncrona principal
