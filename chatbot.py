import os

# Safe import
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit secrets fallback
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = None

# Safe client (FIXED for OpenRouter)
if OPENAI_AVAILABLE and api_key:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://lifeline-ai.streamlit.app",  # can be anything
            "X-Title": "LifeLine AI"
        }
    )
else:
    client = None


SYSTEM_PROMPT = """You are LifeLine Assistant, a helpful AI medical assistant.
Give short, clear first aid advice for burns.
Recommend emergency help for severe burns.
"""


def get_chatbot_response(user_message: str) -> str:
    if client is None:
        return "⚠️ Chatbot not available (API key missing or OpenAI not installed)"

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"API Error: {str(e)}"
