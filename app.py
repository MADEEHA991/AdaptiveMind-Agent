import logging
from datetime import datetime

import streamlit as st

from backend.agent import AdaptiveMind
from backend.conversation import (
    create_conversation,
    add_message,
    get_conversations,
    get_conversation_messages,
    delete_conversation,
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AdaptiveMind AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("AdaptiveMind")


# ============================================================
# AGENT INITIALIZATION
# ============================================================

@st.cache_resource
def get_agent():
    return AdaptiveMind()


try:

    agent = get_agent()

except Exception as exc:

    logger.exception(
        "Failed to initialize AdaptiveMind backend"
    )

    st.error(
        "AdaptiveMind backend could not be initialized."
    )

    st.code(str(exc))

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "conversation_id" not in st.session_state:

    st.session_state.conversation_id = None


if "conversation_title" not in st.session_state:

    st.session_state.conversation_title = None


if "last_response_time" not in st.session_state:

    st.session_state.last_response_time = None


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .memory-card {
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("AdaptiveMind AI")

    st.divider()

    # --------------------------------------------------------
    # NEW CONVERSATION
    # --------------------------------------------------------

    if st.button(
        "New Conversation",
        key="new_conversation",
        use_container_width=True,
    ):

        st.session_state.conversation_id = None

        st.session_state.conversation_title = None

        st.session_state.messages = []

        st.session_state.last_response_time = None

        st.rerun()

    # --------------------------------------------------------
    # CONVERSATION HISTORY
    # --------------------------------------------------------

    st.subheader("Conversation History")

    try:

        conversations = get_conversations()

    except Exception as exc:

        logger.exception(
            "Failed to load conversation history"
        )

        conversations = []

        st.warning(
            "Conversation history is currently unavailable."
        )

    if conversations:

        for conversation in conversations:

            conversation_id = conversation.get("id")

            conversation_title = conversation.get(
                "title",
                "Untitled Conversation",
            )

            # ------------------------------------------------
            # OPEN CONVERSATION
            # ------------------------------------------------

            if st.button(
                conversation_title,
                key=f"conversation_{conversation_id}",
                use_container_width=True,
            ):

                try:

                    loaded_messages = (
                        get_conversation_messages(
                            conversation_id
                        )
                    )

                    st.session_state.conversation_id = (
                        conversation_id
                    )

                    st.session_state.conversation_title = (
                        conversation_title
                    )

                    st.session_state.messages = (
                        loaded_messages
                    )

                    st.session_state.last_response_time = None

                    st.rerun()

                except Exception as exc:

                    logger.exception(
                        "Failed to load conversation"
                    )

                    st.error(
                        "Unable to load this conversation."
                    )

            # ------------------------------------------------
            # DELETE CONVERSATION
            # ------------------------------------------------

            if st.button(
                "Delete",
                key=f"delete_{conversation_id}",
                use_container_width=True,
            ):

                try:

                    delete_conversation(
                        conversation_id
                    )

                    if (
                        st.session_state.conversation_id
                        == conversation_id
                    ):

                        st.session_state.conversation_id = None

                        st.session_state.conversation_title = None

                        st.session_state.messages = []

                        st.session_state.last_response_time = None

                    st.rerun()

                except Exception as exc:

                    logger.exception(
                        "Failed to delete conversation"
                    )

                    st.error(
                        "Unable to delete this conversation."
                    )

    else:

        st.caption(
            "No previous conversations."
        )

    # ========================================================
    # LONG-TERM MEMORY
    # ========================================================

    st.divider()
    st.subheader("Long-Term Memory")

    memory_input = st.text_input(
        "Memory",
        placeholder="Enter something for AdaptiveMind to remember",
        key="memory_input",
    )

    # --------------------------------------------------------
    # SAVE MEMORY
    # --------------------------------------------------------

    if st.button(
        "Save Memory",
        key="save_memory",
        use_container_width=True,
    ):
        memory_text = memory_input.strip()

        if not memory_text:
            st.warning(
                "Please enter something to remember."
            )

        else:
            try:
                agent.save_memory(memory_text)

                st.success(
                    "Memory saved successfully."
                )

                st.rerun()

            except Exception as exc:
                logger.exception(
                    "Failed to save memory"
                )

                st.error(
                    "Unable to save memory."
                )

    # --------------------------------------------------------
    # STORED MEMORIES
    # --------------------------------------------------------

    st.subheader("Stored Memories")

    try:
        memories = agent.get_memories()

    except Exception as exc:
        logger.exception(
            "Failed to retrieve stored memories"
        )

        memories = []

        st.warning(
            "Stored memories are currently unavailable."
        )

    # --------------------------------------------------------
    # MEMORY SELECTION
    # --------------------------------------------------------

    if memories:

        memory_options = {}

        for memory in memories:

            if not isinstance(memory, dict):
                continue

            memory_id = memory.get("id")

            memory_content = memory.get(
                "content",
                memory.get(
                    "text",
                    ""
                ),
            )

            if memory_id and memory_content:

                memory_options[str(memory_id)] = (
                    str(memory_content)
                )

        if memory_options:

            selected_memory_id = st.selectbox(
                "Select a memory",
                options=list(
                    memory_options.keys()
                ),
                format_func=lambda memory_id:
                    memory_options[memory_id],
                key="selected_memory",
            )

            # ------------------------------------------------
            # SELECTED MEMORY
            # ------------------------------------------------

            selected_memory_content = (
                memory_options[
                    selected_memory_id
                ]
            )

            st.caption(
                "Selected memory"
            )

            st.markdown(
                f"""
                <div class="memory-card">
                    {selected_memory_content}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------
            # DELETE SELECTED MEMORY
            # ------------------------------------------------

            if st.button(
                "Delete Memory",
                key="delete_selected_memory",
                use_container_width=True,
            ):

                try:

                    deleted = agent.delete_memory(
                        selected_memory_id
                    )

                    if deleted is False:

                        st.warning(
                            "Selected memory was not found."
                        )

                    else:

                        st.success(
                            "Memory deleted successfully."
                        )

                    st.rerun()

                except Exception as exc:

                    logger.exception(
                        "Failed to delete selected memory"
                    )

                    st.error(
                        "Unable to delete the selected memory."
                    )

        else:

            st.caption(
                "No valid memories available."
            )

    else:

        st.caption(
            "No stored memories."
        )


# ========================================================
# MAIN CHAT AREA
# ========================================================

st.subheader("Chat with AdaptiveMind")


# ========================================================
# DISPLAY CONVERSATION
# ========================================================

for message in st.session_state.messages:

    role = message.get(
        "role"
    )

    content = message.get(
        "content",
        ""
    )

    if role not in {
        "user",
        "assistant",
    }:
        continue

    with st.chat_message(role):

        st.markdown(
            content
        )


# ========================================================
# CHAT INPUT
# ========================================================

user_prompt = st.chat_input(
    "Ask AdaptiveMind AI anything..."
)

if user_prompt:

    user_prompt = user_prompt.strip()

    if not user_prompt:

        st.warning(
            "Please enter a message."
        )

    else:

        # ------------------------------------------------
        # CREATE NEW CONVERSATION
        # ------------------------------------------------

        if (
            st.session_state.conversation_id
            is None
        ):

            conversation_title = (
                user_prompt[:50]
            )

            if len(user_prompt) > 50:

                conversation_title += "..."

            conversation_id = (
                create_conversation(
                    title=conversation_title
                )
            )

            st.session_state.conversation_id = (
                conversation_id
            )

            st.session_state.conversation_title = (
                conversation_title
            )

        # ------------------------------------------------
        # STORE USER MESSAGE
        # ------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_prompt,
                "timestamp": datetime.now().isoformat(),
            }
        )

        add_message(
            conversation_id=(
                st.session_state.conversation_id
            ),
            role="user",
            content=user_prompt,
        )

        # ------------------------------------------------
        # DISPLAY USER MESSAGE
        # ------------------------------------------------

        with st.chat_message("user"):

            st.markdown(
                user_prompt
            )

        # ------------------------------------------------
        # GENERATE RESPONSE
        # ------------------------------------------------

        with st.chat_message("assistant"):

            try:

                start_time = datetime.now()

                with st.spinner(
                    "Thinking..."
                ):

                    response = (
                        agent.generate_response(
                            user_prompt
                        )
                    )

                end_time = datetime.now()

                response_time = (
                    end_time - start_time
                ).total_seconds()

                st.session_state.last_response_time = (
                    response_time
                )

                # ----------------------------------------
                # VALIDATE RESPONSE
                # ----------------------------------------

                if response is None:

                    response = (
                        "I was unable to generate "
                        "a response."
                    )

                response = str(
                    response
                ).strip()

                if not response:

                    response = (
                        "I was unable to generate "
                        "a response."
                    )

                # ----------------------------------------
                # DISPLAY RESPONSE
                # ----------------------------------------

                st.markdown(
                    response
                )

                # ----------------------------------------
                # STORE RESPONSE
                # ----------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                add_message(
                    conversation_id=(
                        st.session_state.conversation_id
                    ),
                    role="assistant",
                    content=response,
                )

            except Exception as exc:

                logger.exception(
                    "Response generation failed"
                )

                st.error(
                    "Something went wrong while "
                    "generating the response."
                )

                logger.error(
                    "Response error: %s",
                    exc,
                )


# ========================================================
# RESPONSE INFORMATION
# ========================================================

if (
    st.session_state.last_response_time
    is not None
):

    st.caption(
        "Response time: "
        f"{st.session_state.last_response_time:.2f} seconds"
    )


# ========================================================
# END OF APPLICATION
# ========================================================