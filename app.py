import streamlit as st

from backend.agent import AdaptiveMind


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AdaptiveMind AI",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# Initialize Agent
# ---------------------------------------------------------

@st.cache_resource
def get_agent():
    return AdaptiveMind()


try:
    agent = get_agent()

except Exception as error:

    st.error(
        "Failed to initialize AdaptiveMind."
    )

    st.exception(error)

    st.stop()


# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Sidebar - Memory Management
# ---------------------------------------------------------

with st.sidebar:

    st.header("Memory")

    memory_text = st.text_area(
        "Enter something for AdaptiveMind to remember",
        height=120,
        placeholder=(
            "Example: My favourite colour is green."
        )
    )

    if st.button(
        "Save Memory",
        use_container_width=True
    ):

        if not memory_text.strip():

            st.warning(
                "Please enter something to remember."
            )

        else:

            try:

                agent.save_memory(
                    memory_text.strip()
                )

                st.success(
                    "Memory saved successfully."
                )

                st.rerun()

            except Exception as error:

                st.error(
                    "Unable to save memory."
                )

                st.exception(error)

    st.divider()

    st.header("Stored Memories")

    memories = agent.get_memories(
        limit=20
    )

    if memories:

        for index, memory in enumerate(
            memories,
            start=1
        ):

            memory_id = memory.get(
                "id"
            )

            content = memory.get(
                "content",
                ""
            )

            created_at = memory.get(
                "created_at",
                ""
            )

            st.write(
                f"**Memory {index}**"
            )

            st.write(
                content
            )

            if created_at:

                st.caption(
                    created_at
                )

            if st.button(
                "Delete",
                key=f"delete_memory_{memory_id}",
                use_container_width=True
            ):

                try:

                    agent.delete_memory(
                        memory_id
                    )

                    st.success(
                        "Memory deleted."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Unable to delete memory."
                    )

                    st.exception(error)

            st.divider()

    else:

        st.info(
            "No memories stored yet."
        )

    # -----------------------------------------------------
    # Clear All Memories
    # -----------------------------------------------------

    if st.button(
        "Clear All Memories",
        use_container_width=True
    ):

        agent.clear_memories()

        st.success(
            "All memories cleared."
        )

        st.rerun()


# ---------------------------------------------------------
# Main Page
# ---------------------------------------------------------

st.title("AdaptiveMind AI")

st.header("Chat with AdaptiveMind")


# ---------------------------------------------------------
# Display Chat History
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ---------------------------------------------------------
# Chat Input
# ---------------------------------------------------------

user_message = st.chat_input(
    "Ask AdaptiveMind anything..."
)


# ---------------------------------------------------------
# Generate AI Response
# ---------------------------------------------------------

if user_message:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):

        st.write(
            user_message
        )

    with st.chat_message("assistant"):

        with st.spinner(
            "AdaptiveMind is thinking..."
        ):

            response = agent.generate_response(
                user_message
            )

        st.write(
            response
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )