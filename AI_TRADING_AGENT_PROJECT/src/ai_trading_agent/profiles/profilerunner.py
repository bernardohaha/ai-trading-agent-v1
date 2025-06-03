import yaml
from ai_trading_agent.core.data_collector import DataCollector
from ai_trading_agent.core.technical_analysis import TechnicalAnalyzer
from ai_trading_agent.core.scoring_engine import ScoringEngine
from ai_trading_agent.core.decision_engine import DecisionEngine
from ai_trading_agent.core.paper_trader import PaperTrader
from ai_trading_agent.core.performance_tracker import PerformanceTracker
from ai_trading_agent.core.telegram_alerts import TelegramAlerts


class ProfileRunner:
    def __init__(self, name, config):
        self.name = name
        self.config = config

        self.symbol = config["symbol"]
        self.timeframe = config["timeframe"]
        self.indicators_config = config["indicators"]
        self.scoring_weights = config["scoring_weights"]
        self.risk_config = config["risk"]

        self.data_collector = DataCollector()
        self.decision_engine = DecisionEngine()
        self.paper_trader = PaperTrader()
        self.performance_tracker = PerformanceTracker()
        self.telegram = TelegramAlerts()
        self.scoring_engine = ScoringEngine(self.scoring_weights)

    def run(self):
        # Buscar os dados OHLCV
        ohlcv = self.data_collector.get_historical_ohlcv(self.symbol, self.timeframe)

        # Aplicar os indicadores técnicos
        technical_analyzer = TechnicalAnalyzer(ohlcv)
        ohlcv_indicators = technical_analyzer.calculate_indicators()

        # Calcular os níveis de Fibonacci (pode ser usado no Scoring futuramente)
        fib_levels = technical_analyzer.calculate_fibonacci_levels()

        # Calcular o score final (passamos o OHLCV atualizado)
        indicator_scores = self.scoring_engine.calculate_score(
            ohlcv_indicators,
            fib_levels,
            zone="BUY ZONE",  # Placeholder (idealmente virá do suporte/resistência)
            renko_trend="UP",  # Placeholder (idealmente virá do Renko)
            current_price=ohlcv_indicators["close"].iloc[-1],
        )

        # Decisão de trading
        decision = self.decision_engine.make_decision(indicator_scores)

        # Paper trade
        self.paper_trader.execute(decision, self.risk_config)

        # Performance tracking
        self.performance_tracker.update(self.name, decision)

        # Alerta Telegram
        self.telegram.send_alert(f"[{self.name}] Decision: {decision}")


def load_profiles(yaml_path):
    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)
    return data["profiles"]


def main():
    print("\n🚀 MULTI-PROFILE ENGINE INICIADO!\n")

    profiles_config = load_profiles("config/profiles.yaml")

    for profile_name, profile_conf in profiles_config.items():
        print(f"\n--- Executando perfil: {profile_name} ---")
        profile = ProfileRunner(profile_name, profile_conf)
        profile.run()


if __name__ == "__main__":
    main()
