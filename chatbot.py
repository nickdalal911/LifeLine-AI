import os
import openai

# Get API key
try:
    import streamlit as st
    openai.api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    openai.api_key = os.getenv("OPENROUTER_API_KEY")

# OpenRouter base URL
openai.api_base = "https://openrouter.ai/api/v1"

def get_chatbot_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for a burn detection medical app."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
