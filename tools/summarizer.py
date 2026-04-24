from tools.base_tool import BaseTool


class TextSummarizerTool(BaseTool):
    """
    Summarizes text using the Claude LLM via the Anthropic SDK.

    Examples of queries this handles:
      - "summarize: [long paragraph]"
      - "tldr: [article text]"
      - "give me a summary of: [text]"
    """

    name = "summarizer"
    description = "Summarizes long text into 2-3 concise sentences using AI."

    def __init__(self, llm_client):
        self.llm = llm_client

    def execute(self, input_data: str) -> str:
        """
        Extract text from input and return an AI-generated summary.
        """
        text_to_summarize = self._extract_text(input_data)

        if len(text_to_summarize.split()) < 10:
            return (
                "❌ The text is too short to summarize. "
                "Please provide at least a paragraph of text."
            )

        prompt = f"""You are a precise text summarizer.

Summarize the following text in 2-3 concise sentences.
Preserve the key ideas. Do not add opinions or information
that is not in the original text.

Text to summarize:
\"\"\"{text_to_summarize}\"\"\"

Summary:"""

        try:
            summary = self.llm.complete(prompt)
            return f"📝 Summary:\n{summary}"
        except Exception as e:
            return f"❌ Summarization failed: {str(e)}"

    def _extract_text(self, input_data: str) -> str:
        """
        Strip instruction prefixes and return the raw text to summarize.
        """
        instruction_words = [
            "summarize this:", "summarize:", "summary of:",
            "give me a summary of:", "tldr:", "summarize this paragraph:",
            "summarize the following:"
        ]
        cleaned = input_data.strip()
        for phrase in instruction_words:
            if cleaned.lower().startswith(phrase):
                cleaned = cleaned[len(phrase):].strip()
                break
        return cleaned