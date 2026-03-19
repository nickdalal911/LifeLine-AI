import os
from openai import OpenAI

# Get API key (Streamlit secrets OR environment variable)
try:
    import streamlit as st
    api_key = st.secrets["OPENROUTER_API_KEY"]  # ✅ use this name
except:
    api_key = os.getenv("OPENROUTER_API_KEY")

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "https://lifeline-ai.streamlit.app",
        "X-Title": "LifeLine AI"
    }
)

# Chatbot function
def get_chatbot_response(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  # ✅ OpenRouter-supported model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for a burn detection medical app. Give clear, safe, and concise advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
