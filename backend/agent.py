import logging
import uuid
from typing import Dict, List

from backend.groq_client import GroqClient
from backend.memory import Memory


# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger("AdaptiveMind")


# ---------------------------------------------------------
# AdaptiveMind Agent
# ---------------------------------------------------------

class AdaptiveMind:
    """
    Main AdaptiveMind AI agent.

    Responsibilities:
    - Communicate with Groq
    - Store long-term memories
    - Retrieve relevant memories
    - Delete individual memories
    - Clear all memories
    - Build memory-aware AI responses
    """

    def __init__(self) -> None:
        """Initialize AdaptiveMind."""

        logger.info(
            "Starting AdaptiveMind"
        )

        self.groq = GroqClient()

        logger.info(
            "Groq client initialized"
        )

        self.memory = Memory()

        logger.info(
            "SQLite memory database initialized"
        )

    # -----------------------------------------------------
    # Save Memory
    # -----------------------------------------------------

    def save_memory(
        self,
        content: str
    ) -> str:
        """
        Save a new memory.

        Returns:
            The unique memory ID.
        """

        if not content or not content.strip():
            raise ValueError(
                "Memory content cannot be empty."
            )

        memory_id = str(
            uuid.uuid4()
        )

        self.memory.add_memory(
            memory_id,
            content.strip()
        )

        logger.info(
            "Memory saved: %s",
            memory_id
        )

        return memory_id

    # -----------------------------------------------------
    # Get Memories
    # -----------------------------------------------------

    def get_memories(
        self,
        limit: int = 20
    ) -> List[Dict]:
        """
        Retrieve stored memories.

        Args:
            limit: Maximum number of memories.

        Returns:
            List of memory dictionaries.
        """

        memories = self.memory.get_memories(
            limit=limit
        )

        logger.info(
            "Retrieved %d memory item(s).",
            len(memories)
        )

        return memories

    # -----------------------------------------------------
    # Search Memory
    # -----------------------------------------------------

    def search_memory(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Search long-term memory using keywords.

        Args:
            query: User's question or search text.
            limit: Maximum number of results.

        Returns:
            Relevant memories.
        """

        results = self.memory.search_memory(
            query=query,
            limit=limit
        )

        logger.info(
            "Memory search completed. Found %d result(s).",
            len(results)
        )

        return results

    # -----------------------------------------------------
    # Delete Individual Memory
    # -----------------------------------------------------

    def delete_memory(
        self,
        memory_id: str
    ) -> None:
        """
        Delete one specific memory.

        Args:
            memory_id: Unique ID of the memory.
        """

        if not memory_id or not memory_id.strip():
            raise ValueError(
                "Memory ID cannot be empty."
            )

        self.memory.delete_memory(
            memory_id.strip()
        )

        logger.info(
            "Memory deleted: %s",
            memory_id
        )

    # -----------------------------------------------------
    # Clear All Memories
    # -----------------------------------------------------

    def clear_memories(self) -> None:
        """Delete all stored memories."""

        self.memory.clear_memories()

        logger.info(
            "All memories cleared."
        )

    # -----------------------------------------------------
    # Build Memory Context
    # -----------------------------------------------------

    def build_memory_context(
        self,
        user_message: str
    ) -> str:
        """
        Build relevant memory context for the AI.

        The agent first searches for memories related
        to the user's current message.

        If no matching memories are found, recent
        memories are used as fallback context.
        """

        relevant_memories = self.search_memory(
            user_message,
            limit=5
        )

        if relevant_memories:

            logger.info(
                "Memory context prepared for user message."
            )

        else:

            relevant_memories = self.get_memories(
                limit=10
            )

            if relevant_memories:

                logger.info(
                    "No direct memory match found. "
                    "Using recent memories as fallback."
                )

        if not relevant_memories:

            return ""

        memory_lines = []

        for memory in relevant_memories:

            content = memory.get(
                "content",
                ""
            ).strip()

            if content:

                memory_lines.append(
                    f"- {content}"
                )

        if not memory_lines:

            return ""

        return "\n".join(
            memory_lines
        )

    # -----------------------------------------------------
    # System Prompt
    # -----------------------------------------------------

    def _build_system_prompt(
        self,
        memory_context: str
    ) -> str:
        """
        Build the system prompt used by the AI.
        """

        base_prompt = """
You are AdaptiveMind AI, a professional personal AI assistant.

Your goal is to provide accurate, useful, clear, and natural
responses to the user.

You have access to long-term memories saved by the user.

Use the supplied memories only when they are relevant to
the user's current question.

Do not claim to remember information that is not present
in the supplied memory context.

If a memory is relevant, use it naturally without repeatedly
mentioning that it came from memory.

If the user asks about something that is not available in
memory, answer normally using your general knowledge.

Be concise for simple questions and provide detailed
explanations when the user asks for more detail.

Never invent personal information about the user.
""".strip()

        if memory_context:

            return (
                f"{base_prompt}\n\n"
                "Relevant long-term memories:\n"
                f"{memory_context}"
            )

        return base_prompt

    # -----------------------------------------------------
    # Generate AI Response
    # -----------------------------------------------------

    def generate_response(
        self,
        user_message: str
    ) -> str:
        """
        Generate an AI response using Groq and memory.
        """

        if not user_message or not user_message.strip():
            raise ValueError(
                "User message cannot be empty."
            )

        user_message = user_message.strip()

        memory_context = self.build_memory_context(
            user_message
        )

        system_prompt = self._build_system_prompt(
            memory_context
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        response = self.groq.chat(
            messages
        )

        if not response or not response.strip():

            raise RuntimeError(
                "The AI returned an empty response."
            )

        logger.info(
            "Response generated successfully."
        )

        return response.strip()