from tools.base_tool import BaseTool


class WebSearchTool(BaseTool):
    """
    Handles web search queries.

    Examples of queries this handles:
      - "search: what is machine learning?"
      - "look up: Python programming language"
      - "find information about: neural networks"
    """

    name = "search"

    def execute(self, input_data: str) -> str:
        search_query = self._extract_query(input_data)

        if not search_query:
            return "❌ Please provide a search query."

        return self._mock_search(search_query)

    def _extract_query(self, input_data: str) -> str:
        prefixes = [
            "search:", "search for:", "look up:", "find:",
            "find information about:", "what is", "who is"
        ]
        cleaned = input_data.strip()
        for prefix in prefixes:
            if cleaned.lower().startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                break
        return cleaned

    def _mock_search(self, query: str) -> str:
        mock_database = {
            "python": (
                "Python is a high-level, interpreted programming language "
                "known for its clear syntax and readability. Created by Guido "
                "van Rossum in 1991, it is widely used in web development, "
                "data science, AI/ML, automation, and scientific computing."
            ),
            "machine learning": (
                "Machine Learning is a subset of AI that enables systems to "
                "learn and improve from experience without being explicitly "
                "programmed. It focuses on developing programs that can access "
                "data and use it to learn for themselves."
            ),
            "neural network": (
                "A neural network is a series of algorithms that attempt to "
                "recognize patterns in data through a process that mimics how "
                "the human brain operates. Used extensively in image recognition, "
                "NLP, and generative AI."
            ),
            "api": (
                "An API (Application Programming Interface) is a set of rules "
                "that allow different software applications to communicate. "
                "It defines the methods and data formats that applications can "
                "use to request and exchange information."
            ),
            "anthropic": (
                "Anthropic is an AI safety company founded in 2021 by Dario "
                "Amodei, Daniela Amodei, and other former OpenAI researchers. "
                "They develop Claude, a family of AI assistants focused on "
                "being helpful, harmless, and honest."
            ),
        }

        query_lower = query.lower()
        for keyword, result in mock_database.items():
            if keyword in query_lower:
                return (
                    f"🔍 Search results for: '{query}'\n\n"
                    f"{result}\n\n"
                    f"[Source: SmartAssist Knowledge Base — Mock Data]"
                )

        return (
            f"🔍 Search results for: '{query}'\n\n"
            f"This topic is recognized as a valid search query. "
            f"In a production environment, this would return live web results. "
            f"For now, consider '{query}' as a concept worth exploring further "
            f"through documentation or tutorials.\n\n"
            f"[Source: SmartAssist Knowledge Base — Mock Data]"
        )