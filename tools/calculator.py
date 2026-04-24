import re
from tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """
    Evaluates mathematical expressions from a user query.

    Examples of queries this handles:
      - "calculate 25 * 18"
      - "what is 100 / 4 + 37?"
      - "347 * 19 + 88"
    """

    name = "calculator"

    def execute(self, input_data: str) -> str:
        """
        Extract and evaluate a mathematical expression from the input.
        """
        expression = self._extract_expression(input_data)

        if not expression:
            return (
                "❌ I couldn't find a valid mathematical expression. "
                "Please include numbers and operators (e.g., '25 * 4 + 10')."
            )

        try:
            safe_expr = re.sub(r"[^0-9+\-*/().\s]", "", expression)
            result = eval(safe_expr)  # noqa: S307
            return f"🧮 Expression: {safe_expr.strip()}\n   Result: {result:,}"

        except ZeroDivisionError:
            return "❌ Error: Division by zero is not allowed."
        except Exception as e:
            return f"❌ Calculation failed: {str(e)}"

    def _extract_expression(self, text: str) -> str:
        """
        Remove instruction words and return just the math expression.
        """
        prefixes = ["calculate", "compute", "what is", "evaluate", "solve"]
        cleaned = text.lower()
        for prefix in prefixes:
            cleaned = cleaned.replace(prefix, "")

        match = re.search(r"[\d\s\+\-\*\/\(\)\.]+", cleaned)
        return match.group(0).strip() if match else ""