import sys
import os

# Garantir que o src/ está no sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

# Agora podemos importar o ProfileRunner
from ai_trading_agent.profiles.profilerunner import ProfileRunner, load_profiles


def test_run():
    print("\n🚀 TEST RUN MULTI-PROFILE ENGINE INICIADO!\n")

    profiles_config = load_profiles("src/ai_trading_agent/config/profiles.yaml")

    for profile_name, profile_conf in profiles_config.items():
        print(f"\n--- Executando profile: {profile_name.upper()} ---")

        try:
            profile = ProfileRunner(profile_name, profile_conf)
            profile.run()
            print(f"✅ {profile_name} executado com sucesso.\n")

        except Exception as e:
            print(f"❌ Erro ao executar {profile_name}: {str(e)}")


if __name__ == "__main__":
    test_run()
