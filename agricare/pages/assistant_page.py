
import streamlit as st

from agricare.services.ai_assistant import get_ai_response


def render_assistant_page(user):

    st.markdown(
        '<div class="main-title">AgriCare AI Assistant 🤖</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your intelligent AI companion for farming and beyond.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Initialize conversation

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": (
                    "Namaste! 🌱 Welcome to AgriCare AI.\n\n"
                    "I am powered by Gemini AI. You can ask me about "
                    "potato farming, diseases, irrigation, fertilizers, "
                    "technology, science or any general topic.\n\n"
                    "How can I help you today?"
                )
            }
        ]

    # Clear conversation

    col1, col2 = st.columns([5, 1])

    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state["chat_messages"] = []
            st.rerun()

    # Display previous messages

    for message in st.session_state["chat_messages"]:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input

    prompt = st.chat_input(
        "Message AgriCare AI..."
    )

    if prompt:

        # Display user message

        st.session_state["chat_messages"].append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response

        with st.chat_message("assistant"):

            with st.spinner("AgriCare AI is thinking..."):

                response = get_ai_response(
                    st.session_state["chat_messages"]
                )

            st.markdown(response)

        # Save AI response

        st.session_state["chat_messages"].append({
            "role": "assistant",
            "content": response
        })

    st.divider()

    st.caption(
        "Powered by Google Gemini AI | "
        "AI-generated agricultural guidance should be verified "
        "with qualified agricultural experts."
    )
