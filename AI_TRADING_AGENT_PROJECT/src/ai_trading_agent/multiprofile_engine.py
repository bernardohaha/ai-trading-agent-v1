import yaml

from ai_trading_agent.core.data_collector import DataCollector
from ai_trading_agent.core.scoring_engine import ScoringEngine
from ai_trading_agent.core.technical_analysis import TechnicalAnalyzer
from ai_trading_agent.core.decision_engine import DecisionEngine
from ai_trading_agent.core.paper_trader import PaperTrader
from ai_trading_agent.core.performance_tracker import PerformanceTracker
from ai_trading_agent.core.telegram_alerts import TelegramAlerts
from ai_trading_agent.profiles.profilerunner import ProfileRunner


class ProfileRunner:
    def __init__(self, name, config):
        self.name = name
        self.config = config

        self.symbol = config["symbol"]
        self.timeframe = config["timeframe"]
        self.data_collector = DataCollector()
        self.technical_analyzer = TechnicalAnalyzer()  # Novo: usamos o teu engine real
        self.scoring_engine = ScoringEngine()
        self.decision_engine = DecisionEngine()
        self.paper_trader = PaperTrader()
        self.performance_tracker = PerformanceTracker()
        self.telegram = TelegramAlerts()

    def run(self):
        # Fetch data
        ohlcv = self.data_collector.fetch_data(self.symbol, self.timeframe)

        # Análise técnica (apenas exemplo: adaptar com a tua lógica real de indicators)
        indicators = self.technical_analyzer.calculate_indicators(
            ohlcv, self.config["indicators"]
        )

        # Calcular score
        score = self.scoring_engine.calculate(
            indicators, self.config["scoring_weights"]
        )

        # Decisão
        decision = self.decision_engine.make_decision(score)

        # Executar trade
        self.paper_trader.execute(decision, self.config["risk"])

        # Atualizar performance
        self.performance_tracker.update(self.name, decision)

        # Alertas Telegram
        self.telegram.send_alert(f"[{self.name}] Decision: {decision}")


def load_profiles(yaml_path):
    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)
    return data["profiles"]


def main():
    print("\n🚀 MULTIPROFILE ENGINE INICIADO COM SUCESSO!\n")

    profiles_config = load_profiles("config/profiles.yaml")

    for profile_name, profile_conf in profiles_config.items():
        print(f"\n--- Executando perfil: {profile_name} ---")
        profile = ProfileRunner(profile_name, profile_conf)
        profile.run()


if __name__ == "__main__":
    main()
