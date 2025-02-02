# **For Deploying on Render**
import requests
import streamlit as st
from streamlit.components.v1 import html
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
def init_groq_client(api_key, api_url):
    return {
        "api_key": api_key,
        "api_url": api_url
    }

# Function to get responses from Groq API
def get_groq_response(prompt, model="mixtral-8x7b-32768",api_key=None, api_url=None):
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY")
    if not api_url:
        api_url = os.environ.get("GROQ_API_URL")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": prompt
        }],
        "temperature": 0.7
    }

    response = requests.post(
        api_url,
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}"

# Streamlit app
st.title("💬 AI Chatbot - Poverty Combat Assistance")
st.write("Ask me anything about unemployment solutions, addressing poverty, aid programs, or donations!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What would you like to discuss?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from Groq
    with st.chat_message("assistant"):
        # st.markdown("Think")
        response = get_groq_response(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add loading spinner
with st.spinner("Processing your request..."):
    pass