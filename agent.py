from tools.base_tool import BaseTool
from llm.client import LLMClient


class Agent:
    """
    The orchestrating brain of SmartAssist.
    """

    def __init__(self, tools: list[BaseTool], llm_client: LLMClient):
        self.llm = llm_client
        self.tools: dict[str, BaseTool] = {
            tool.name: tool for tool in tools
        }

        print(f"[Agent] Initialized with tools: {list(self.tools.keys())}")

    def decide_tool(self, query: str) -> str:
        """
        Use the LLM to decide which tool is best for the query.
        """
        tool_names = list(self.tools.keys())
        tool_list = "\n".join(f"- {name}" for name in tool_names)

        decision_prompt = f"""You are the routing system for an AI agent called SmartAssist.

Your ONLY job is to select the most appropriate tool for the user's query.

Available tools:
{tool_list}

Tool descriptions:
- calculator: Use for any mathematical calculation, arithmetic, or numerical computation
- summarizer: Use for summarizing, condensing, or explaining a piece of text
- search: Use for factual questions, looking up information, or general knowledge queries

User query: "{query}"

Instructions:
1. Analyze the user's intent carefully
2. Select exactly ONE tool from the list above
3. Respond with ONLY the tool name — nothing else, no punctuation, no explanation

Tool selection:"""

        raw_decision = self.llm.complete(decision_prompt, max_tokens=20)
        cleaned = raw_decision.strip().lower().rstrip(".")

        if cleaned in self.tools:
            return cleaned

        for tool_name in tool_names:
            if tool_name in cleaned:
                return tool_name

        print(f"[Agent Warning] Unrecognized tool '{cleaned}'. Defaulting to 'search'.")
        return "search"

    def run(self, query: str) -> str:
        """
        The main execution pipeline: decide → execute → return.
        """
        if not query.strip():
            return "❌ Please enter a valid query."

        print(f"\n[🤖 Agent thinking... selecting tool]", flush=True)
        tool_name = self.decide_tool(query)

        tool = self.tools[tool_name]
        print(f"[🔧 Running: {tool.__class__.__name__}]", flush=True)

        try:
            result = tool.execute(query)
            return result
        except Exception as e:
            return (
                f"❌ An error occurred while running the {tool_name} tool:\n"
                f"   {type(e).__name__}: {str(e)}"
            )