import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """
    A clean wrapper around the Groq SDK.
    """

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY not found.\n"
                "Make sure your .env file exists and contains:\n"
                "GROQ_API_KEY=gsk_your-key-here"
            )

        self.client = Groq(api_key=api_key)
        self.model = model
        self.max_tokens = 1024

    def complete(self, prompt: str, max_tokens: int = None) -> str:
        """
        Send a prompt to the LLM and return the text response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"\n[LLMClient Error] API call failed: {type(e).__name__}: {e}")
            raise