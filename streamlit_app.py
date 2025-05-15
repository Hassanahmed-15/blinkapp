import os
import streamlit as st
from google import genai
from google.genai.types import HttpOptions

# ─── Streamlit page setup ─────────────────────────────────────────────
st.set_page_config(page_title="LLM Agent", layout="wide")

# ─── Gemini configuration ────────────────────────────────────────────
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("🔑 Please set the GEMINI_API_KEY environment variable and restart.")
    st.stop()

# Use the Gen AI SDK client in “express” mode (with just API key):
client = genai.Client(vertexai=True, api_key=API_KEY)

# ─── Session memory ────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []  # list of (role, message) tuples

# ─── LLM call helper ───────────────────────────────────────────────────
def ask_gemini(question: str) -> str:
    # Build the chat history in Gemini’s “chat” format:
    messages = []
    for role, msg in st.session_state.history:
        messages.append({"role": role, "content": msg})
    messages.append({"role": "user", "content": question})

    # Call the Gemini model:
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",      # adjust to your exact model name
        contents=messages
    )
    return resp.text

# ─── UI: Chat Input ───────────────────────────────────────────────────
st.title("🎙️ LLM Agent")
user_input = st.text_input("Your question:", key="input")
if st.button("Send") and user_input:
    st.session_state.history.append(("user", user_input))
    with st.spinner("🤖 Thinking..."):
        bot_response = ask_gemini(user_input)
    st.session_state.history.append(("assistant", bot_response))
    st.session_state.input = ""

# ─── Render the conversation ─────────────────────────────────────────
for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Agent:** {msg}")
