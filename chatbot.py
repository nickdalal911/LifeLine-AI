import os
from openai import OpenAI

# Get key (this WILL work with Streamlit secrets)
try:
    import streamlit as st
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "https://lifeline-ai.streamlit.app",
        "X-Title": "LifeLine AI"
    }
)

import os
from openai import OpenAI

# Get key (this WILL work with Streamlit secrets)
try:
    import streamlit as st
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "https://lifeline-ai.streamlit.app",
        "X-Title": "LifeLine AI"
    }
)
