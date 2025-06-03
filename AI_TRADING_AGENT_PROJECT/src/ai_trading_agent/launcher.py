from ai_trading_agent.core.run_agent import main as run_agent_main
from ai_trading_agent.core.live_agent import main as live_agent_main
from ai_trading_agent.core.frontend_streamlit import main as streamlit_main
from ai_trading_agent.core.run_backtest import main as run_backtest_main
from ai_trading_agent.core.run_optimizer import main as run_optimizer_main


def launcher():
    print("""
    ==================================
         AI TRADING AGENT LAUNCHER
    ==================================
    1 - Run Live Agent
    2 - Run Streamlit Frontend
    3 - Run Backtest
    4 - Run Optimizer
    5 - Run Full Agent
    """)

    choice = input("Escolha a opo: ")

    if choice == "1":
        live_agent_main()
    elif choice == "2":
        streamlit_main()
    elif choice == "3":
        run_backtest_main()
    elif choice == "4":
        run_optimizer_main()
    elif choice == "5":
        run_agent_main()
    else:
        print("Opo invlida.")


if __name__ == "__main__":
    launcher()
