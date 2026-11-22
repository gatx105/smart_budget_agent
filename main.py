"""Application entry point for the smart budget agent."""

from agent.core import SmartBudgetAgent
from database.db_setup import initialize_database


def main() -> None:
    """Start the command-line interaction loop."""
    initialize_database()
    agent = SmartBudgetAgent()
    print("智慧記帳 Agent 已啟動，輸入 exit 離開。")

    while True:
        user_input = input("你：").strip()
        if user_input.lower() == "exit":
            break
        print(f"Agent：{agent.handle(user_input)}")


if __name__ == "__main__":
    main()