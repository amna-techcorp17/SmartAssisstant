from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Abstract base class for all SmartAssist tools.

    Every tool must inherit from this class and implement
    the `execute` method.
    """

    name: str = "base_tool"
    description: str = "A base tool with no functionality."

    @abstractmethod
    def execute(self, input_data: str) -> str:
        """
        Execute the tool with the given input.

        Args:
            input_data: The raw user query or processed input string.

        Returns:
            A formatted string response to display to the user.
        """

    def __repr__(self) -> str:
        return f"<Tool name='{self.name}' description='{self.description}'>"