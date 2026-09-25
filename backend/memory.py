import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Memory:
    """SQLite-based long-term memory manager for AdaptiveMind AI."""

    def __init__(self) -> None:
        """Initialize the persistent memory database."""

        self.base_dir = Path(__file__).resolve().parent.parent

        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.database_path = (
            self.data_dir / "adaptive_memory.db"
        )

        self._initialize_database()

    # =====================================================
    # DATABASE CONNECTION
    # =====================================================

    def _connect(self) -> sqlite3.Connection:
        """Create a SQLite database connection."""

        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        return connection

    # =====================================================
    # DATABASE INITIALIZATION
    # =====================================================

    def _initialize_database(self) -> None:
        """Create the memories table if it does not exist."""

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()

            # -------------------------------------------------
            # DATABASE MIGRATION
            # -------------------------------------------------
            #
            # Older versions of AdaptiveMind may not have
            # updated_at. Add it safely if necessary.
            #

            columns = connection.execute(
                """
                PRAGMA table_info(memories)
                """
            ).fetchall()

            column_names = {
                column["name"]
                for column in columns
            }

            if "updated_at" not in column_names:

                connection.execute(
                    """
                    ALTER TABLE memories
                    ADD COLUMN updated_at
                    TIMESTAMP
                    """
                )

                connection.execute(
                    """
                    UPDATE memories
                    SET updated_at = created_at
                    WHERE updated_at IS NULL
                    """
                )

                connection.commit()

    # =====================================================
    # MEMORY TYPE DETECTION
    # =====================================================

    def _extract_preference_key(
        self,
        content: str
    ) -> Optional[str]:
        """
        Detect a simple user preference.

        Example:

        My favorite programming language is Python.

        returns:

        favorite programming language
        """

        if not content:
            return None

        text = content.strip().lower()

        patterns = [
            r"my\s+favorite\s+(.+?)\s+is\s+",
            r"my\s+favourite\s+(.+?)\s+is\s+",
            r"i\s+prefer\s+(.+?)\s+over\s+",
            r"i\s+prefer\s+(.+?)\s+to\s+",
            r"my\s+preferred\s+(.+?)\s+is\s+",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                key = match.group(1).strip()

                key = re.sub(
                    r"\s+",
                    " ",
                    key
                )

                if key:
                    return key

        return None

    # =====================================================
    # ADD OR UPDATE MEMORY
    # =====================================================

    def add_memory(
        self,
        memory_id: str,
        content: str
    ) -> None:
        """
        Add a new memory.

        If the memory represents a preference that already
        exists, update the existing preference instead of
        creating a duplicate conflicting memory.
        """

        if not memory_id or not memory_id.strip():

            raise ValueError(
                "Memory ID cannot be empty."
            )

        if not content or not content.strip():

            raise ValueError(
                "Memory content cannot be empty."
            )

        memory_id = memory_id.strip()
        content = content.strip()

        preference_key = self._extract_preference_key(
            content
        )

        with self._connect() as connection:

            # -------------------------------------------------
            # HANDLE PREFERENCE UPDATES
            # -------------------------------------------------

            if preference_key:

                memories = connection.execute(
                    """
                    SELECT id, content
                    FROM memories
                    """
                ).fetchall()

                existing_memory_id = None

                for memory in memories:

                    existing_key = (
                        self._extract_preference_key(
                            memory["content"]
                        )
                    )

                    if (
                        existing_key
                        and existing_key == preference_key
                    ):
                        existing_memory_id = memory["id"]
                        break

                # ---------------------------------------------
                # UPDATE EXISTING PREFERENCE
                # ---------------------------------------------

                if existing_memory_id:

                    connection.execute(
                        """
                        UPDATE memories
                        SET
                            content = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (
                            content,
                            existing_memory_id
                        )
                    )

                    connection.commit()

                    return

            # -------------------------------------------------
            # ADD NEW MEMORY
            # -------------------------------------------------

            connection.execute(
                """
                INSERT OR REPLACE INTO memories
                (
                    id,
                    content,
                    created_at,
                    updated_at
                )
                VALUES (
                    ?,
                    ?,
                    CURRENT_TIMESTAMP,
                    CURRENT_TIMESTAMP
                )
                """,
                (
                    memory_id,
                    content
                )
            )

            connection.commit()

    # =====================================================
    # GET MEMORIES
    # =====================================================

    def get_memories(
        self,
        limit: int = 20
    ) -> List[Dict]:
        """Retrieve the most recently updated memories."""

        if limit <= 0:
            return []

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT
                    id,
                    content,
                    created_at,
                    updated_at
                FROM memories
                ORDER BY
                    datetime(updated_at) DESC,
                    rowid DESC
                LIMIT ?
                """,
                (limit,)
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "content": row["content"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            for row in rows
        ]

    # =====================================================
    # KEYWORD EXTRACTION
    # =====================================================

    def _extract_keywords(
        self,
        query: str
    ) -> List[str]:
        """Extract meaningful keywords from a query."""

        words = re.findall(
            r"[a-zA-Z0-9+#.]+",
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
            "or",
            "isn't",
            "isnt",
        }

        keywords = [
            word
            for word in words
            if word not in stop_words
            and len(word) > 1
        ]

        return keywords

    # =====================================================
    # MEMORY SEARCH
    # =====================================================

    def search_memory(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Search memories using keyword matching.

        More relevant memories receive higher scores.
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
                    r"[a-zA-Z0-9+#.]+",
                    content.lower()
                )
            )

            score = 0

            for keyword in keywords:

                if keyword in content_words:

                    score += 1

            # ---------------------------------------------
            # Preference relevance
            # ---------------------------------------------

            preference_key = (
                self._extract_preference_key(
                    content
                )
            )

            query_lower = query.lower()

            if (
                preference_key
                and preference_key in query_lower
            ):
                score += 3

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
                    "updated_at",
                    item[1].get(
                        "created_at",
                        ""
                    )
                )
            ),
            reverse=False
        )

        return [
            memory
            for _, memory in scored_memories[:limit]
        ]

    # =====================================================
    # DELETE INDIVIDUAL MEMORY
    # =====================================================

    def delete_memory(
        self,
        memory_id: str
    ) -> bool:
        """
        Delete one specific memory.

        Returns True if a memory was deleted.
        """

        if not memory_id or not memory_id.strip():

            raise ValueError(
                "Memory ID cannot be empty."
            )

        with self._connect() as connection:

            cursor = connection.execute(
                """
                DELETE FROM memories
                WHERE id = ?
                """,
                (
                    memory_id.strip(),
                )
            )

            connection.commit()

            return cursor.rowcount > 0

    # =====================================================
    # CLEAR ALL MEMORIES
    # =====================================================

    def clear_memories(self) -> None:
        """Delete all stored memories."""

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM memories
                """
            )

            connection.commit()

    # =====================================================
    # MEMORY COUNT
    # =====================================================

    def memory_count(self) -> int:
        """Return the total number of stored memories."""

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT COUNT(*)
                FROM memories
                """
            )

            result = cursor.fetchone()

        return int(result[0])