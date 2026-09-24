import os
from typing import Dict, List

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class GroqClient:
    """Client for communicating with the Groq API."""

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is missing from the .env file."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = "openai/gpt-oss-120b"

    def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """Send a conversation to Groq."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content or ""