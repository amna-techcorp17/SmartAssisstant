import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """
    A clean wrapper around the Anthropic SDK.
    """

    def __init__(self, model: str = "claude-3-5-haiku-20241022"):
        api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not found.\n"
                "Make sure your .env file exists and contains:\n"
                "ANTHROPIC_API_KEY=sk-ant-your-key-here"
            )

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = 1024
        self.temperature = 0.3

    def complete(self, prompt: str, max_tokens: int = None) -> str:
        """
        Send a prompt to the LLM and return the text response.
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            print(f"\n[LLMClient Error] API call failed: {type(e).__name__}: {e}")
            raise