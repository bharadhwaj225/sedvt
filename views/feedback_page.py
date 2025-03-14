import streamlit as st
import pymongo
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components

load_dotenv()

# Connect to MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    st.error("MongoDB URI not found! Please check your .env file.")
    st.stop()

client = pymongo.MongoClient(MONGODB_URI)
db = client['feedback_db']
collection = db['data_corrections']

# Custom CSS for better styling
st.markdown(
    """
    <style>
    body {
        background-color: #F0F2F6;
        font-family: Arial, sans-serif;
    }
    .feedback-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: 2rem auto;
    }
    .feedback-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #333333;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .feedback-subheader {
        font-size: 1.2rem;
        color: #555555;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h1 class='feedback-header'>Help Us To Improve Our Data!</h1>", unsafe_allow_html=True)
st.markdown("<p class='feedback-subheader'>If you notice any incorrect data in our AI-Powered Socio-Economic Data Visualization and Predictive Analytics Tool, please let us know. Your input helps us ensure data accuracy and improve our insights.</p>", unsafe_allow_html=True)

# feedback submission
with st.form("correction_form", clear_on_submit=True):
    name = st.text_input("Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="example@domain.com")
    feedback = st.text_area("Describe the Data Issue", placeholder="Explain the incorrect data or suggest a correction")
    submit_button = st.form_submit_button("Submit Feedback")
st.markdown("</div>", unsafe_allow_html=True)

components.html(
    """
    <script>
    const formContainer = document.getElementById('correction_form_container');
    if(formContainer){
        formContainer.addEventListener('keydown', function(event) {
            // Prevent Enter key submission in inputs and select fields
            if (event.key === 'Enter' && event.target.tagName !== 'TEXTAREA') {
                event.preventDefault();
            }
        });
    }
    </script>
    """,
    height=0,
)

# Validate and process form submission
if submit_button:
    errors = []
    if not name.strip():
        errors.append("Name field cannot be empty.")
    if not feedback.strip():
        errors.append("Please describe the data issue in detail.")
    elif len(feedback.strip()) < 25:
        errors.append("Feedback must be at least 25 characters long.")
        
    if errors:
        for error in errors:
            st.error(error)
    else:
        document = {
            "name": name,
            "email": email,
            "feedback": feedback
        }
        try:
            result = collection.insert_one(document)
            if result.inserted_id:
                st.success("Thank you! Your data correction feedback has been recorded. We will review your suggestion and update the data if necessary.")
            else:
                st.error("An error occurred while submitting your feedback. Please try again later.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
