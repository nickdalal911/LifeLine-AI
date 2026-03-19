from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# fallback for deployment
if not api_key:
    api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

SYSTEM_PROMPT = """You are LifeLine Assistant, a helpful AI medical assistant.
Give short, clear first aid advice for burns.
Recommend emergency help for severe burns.
"""

def get_chatbot_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",  # ✅ FIXED MODEL
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
