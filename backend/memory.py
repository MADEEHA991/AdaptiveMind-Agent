import re
import sqlite3
from pathlib import Path
from typing import Dict, List


class Memory:
    """SQLite-based long-term memory manager."""

    def __init__(self) -> None:
        """Initialize the memory database."""

        self.data_dir = Path("data")

        self.data_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.database_path = (
            self.data_dir / "adaptive_memory.db"
        )

        self._initialize_database()

    # -----------------------------------------------------
    # Database Connection
    # -----------------------------------------------------

    def _connect(self):
        """Create a SQLite database connection."""

        return sqlite3.connect(
            self.database_path
        )

    # -----------------------------------------------------
    # Database Initialization
    # -----------------------------------------------------

    def _initialize_database(self) -> None:
        """Create the memories table if it does not exist."""

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()

    # -----------------------------------------------------
    # Add Memory
    # -----------------------------------------------------

    def add_memory(
        self,
        memory_id: str,
        content: str
    ) -> None:
        """Add a new memory."""

        if not content or not content.strip():

            raise ValueError(
                "Memory content cannot be empty."
            )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO memories
                (id, content)
                VALUES (?, ?)
                """,
                (
                    memory_id,
                    content.strip()
                )
            )

            connection.commit()

    # -----------------------------------------------------
    # Get Memories
    # -----------------------------------------------------

    def get_memories(
        self,
        limit: int = 20
    ) -> List[Dict]:
        """Retrieve the most recent memories."""

        if limit <= 0:
            return []

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT id, content, created_at
                FROM memories
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,)
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "content": row[1],
                "created_at": row[2]
            }
            for row in rows
        ]

    # -----------------------------------------------------
    # Keyword Extraction
    # -----------------------------------------------------

    def _extract_keywords(
        self,
        query: str
    ) -> List[str]:
        """Extract meaningful keywords from a query."""

        words = re.findall(
            r"[a-zA-Z]+",
            query.lower()
        )

        stop_words = {
            "what",
            "is",
            "my",
            "me",
            "i",
            "am",
            "the",
            "a",
            "an",
            "do",
            "does",
            "did",
            "you",
            "can",
            "could",
            "would",
            "should",
            "tell",
            "about",
            "which",
            "who",
            "where",
            "when",
            "why",
            "how",
            "please",
            "remember",
            "like",
            "favourite",
            "favorite",
            "your",
            "tell",
            "know",
            "something",
            "there",
            "are",
            "was",
            "were",
            "have",
            "has",
            "had",
            "to",
            "of",
            "for",
            "in",
            "on",
            "with",
            "and",
            "or"
        }

        keywords = [
            word
            for word in words
            if word not in stop_words
            and len(word) > 2
        ]

        return keywords

    # -----------------------------------------------------
    # Keyword Memory Search
    # -----------------------------------------------------

    def search_memory(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Search memories using keyword matching.

        Memories containing more matching keywords
        receive a higher relevance score.
        """

        if not query or not query.strip():

            return []

        if limit <= 0:

            return []

        keywords = self._extract_keywords(
            query
        )

        if not keywords:

            return []

        memories = self.get_memories(
            limit=1000
        )

        scored_memories = []

        for memory in memories:

            content = memory.get(
                "content",
                ""
            )

            content_words = set(
                re.findall(
                    r"[a-zA-Z]+",
                    content.lower()
                )
            )

            score = 0

            for keyword in keywords:

                if keyword in content_words:

                    score += 1

            if score > 0:

                scored_memories.append(
                    (
                        score,
                        memory
                    )
                )

        scored_memories.sort(
            key=lambda item: (
                -item[0],
                item[1].get(
                    "created_at",
                    ""
                )
            )
        )

        return [
            memory
            for _, memory in scored_memories[:limit]
        ]

    # -----------------------------------------------------
    # Delete Individual Memory
    # -----------------------------------------------------

    def delete_memory(
        self,
        memory_id: str
    ) -> None:
        """Delete one specific memory."""

        if not memory_id or not memory_id.strip():

            raise ValueError(
                "Memory ID cannot be empty."
            )

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM memories
                WHERE id = ?
                """,
                (
                    memory_id.strip(),
                )
            )

            connection.commit()

    # -----------------------------------------------------
    # Clear All Memories
    # -----------------------------------------------------

    def clear_memories(self) -> None:
        """Delete all stored memories."""

        with self._connect() as connection:

            connection.execute(
                "DELETE FROM memories"
            )

            connection.commit()
