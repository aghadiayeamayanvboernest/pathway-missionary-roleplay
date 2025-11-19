import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Pathway-missionary-roleplay",
    page_icon="💬",
    layout="centered"
)

# Initialize OpenAI client
# Try to get API key from Streamlit secrets first, then fall back to environment variable
try:
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
except:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Custom CSS for action buttons
st.markdown(
    """
    <style>
    /* Make action buttons more subtle and elegant */
    div[data-testid="column"] button {
        transition: all 0.2s ease;
        opacity: 0.6;
    }
    div[data-testid="column"] button:hover {
        opacity: 1;
        transform: scale(1.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# App title - centered
st.markdown(
    """
    <div style="text-align: center;">
        <h1>💬 Pathway-missionary-roleplay</h1>
        <p style="color: #666; font-size: 0.9em;">A chatbot powered by OpenAI's GPT-5.1 with conversation memory</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar with clear history button
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Conversation", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Model: GPT-5.1")
    st.caption("Reasoning: none (fast)")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome screen when no messages OR display chat history
if len(st.session_state.messages) == 0:
    # Get current hour to determine greeting
    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good Morning! ☀️"
    elif current_hour < 18:
        greeting = "Good Afternoon! 🌤️"
    else:
        greeting = "Good Evening! 🌙"

    # Center the welcome message
    st.markdown(
        f"""
        <div style="text-align: center; padding: 100px 20px;">
            <h2>{greeting}</h2>
            <p style="font-size: 1.1em; color: #666;">Welcome to Pathway Missionary Roleplay. How can I help you today?</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # Display all previous messages
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Action buttons row with subtle styling
            cols = st.columns([0.9, 0.05, 0.05])

            with cols[1]:
                if st.button("⎘", key=f"copy_{idx}", help="Copy message", use_container_width=True):
                    st.toast("Copied!", icon="✅")

            # Only show regenerate for assistant messages
            if message["role"] == "assistant":
                with cols[2]:
                    if st.button("↻", key=f"regen_{idx}", help="Regenerate response", use_container_width=True):
                        # Remove messages from this point and regenerate
                        st.session_state.messages = st.session_state.messages[:idx]
                        st.rerun()

# Chat input
if prompt := st.chat_input("What would you like to talk about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Rerun immediately to hide welcome screen
    st.rerun()

# Generate response if last message is from user
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare messages for API
                api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]

                # Call OpenAI Responses API with full conversation history
                response = client.responses.create(
                    model="gpt-5.1",
                    input=api_messages,
                    reasoning={"effort": "none"}  # Fast response mode
                )

                # Extract assistant's reply
                assistant_message = response.output_text

                # Display and add assistant response to chat history
                st.markdown(assistant_message)
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                st.rerun()

            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)
                # Add error to chat history
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                st.rerun()
