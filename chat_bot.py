import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    st.error("API Key not found! Check your .env file.")
    st.stop()

CSV_FILE_PATH = "data/data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(CSV_FILE_PATH)

df = load_data()
csv_data_text = df.to_string()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI
st.title("AI Powered Chatbot")
st.write(  
    "Welcome to the AI Powered Chatbot.\n"
    "Simply ask a question, and the AI will analyze the data for you. Whether you're exploring trends,\t"  
    "finding key statistics, or understanding relationships, this chatbot is here to assist you.\n\n "  
    "Start by typing your query below! 💡"  
)


# Chat History
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Handle greetings separately
    greetings = ["hi", "hello", "hey", "greetings"]
    if prompt.lower() in greetings:
        reply = "Hello! 😊 Would you like to ask a specific question or explore the data further? I'm here to help!"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    # API Request
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": f"Use this dataset:\n{csv_data_text}"},
        ] + st.session_state.messages
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
    else:
        st.error(f"⚠️ API Error: {response.text}")