from llm.client import LLMClient
from agent import Agent
from tools.calculator import CalculatorTool
from tools.summarizer import TextSummarizerTool
from tools.search import WebSearchTool


def main():
    print("=" * 55)
    print("   🤖  SmartAssist — AI Agent")
    print("=" * 55)
    print("Type your query below. Type 'exit' or 'quit' to stop.\n")

    try:
        llm_client = LLMClient()
    except EnvironmentError as e:
        print(f"\n❌ Startup Error:\n{e}")
        return

    tools = [
        CalculatorTool(),
        TextSummarizerTool(llm_client=llm_client),
        WebSearchTool(),
    ]

    agent = Agent(tools=tools, llm_client=llm_client)

    print("\n✅ SmartAssist is ready!\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "bye", "goodbye"}:
            print("\n👋 Goodbye! Have a great day!")
            break

        response = agent.run(user_input)
        print(f"\nSmartAssist: {response}\n")
        print("-" * 55)


if __name__ == "__main__":
    main()