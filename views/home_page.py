import streamlit as st

st.set_page_config(layout="wide")

st.title("Socio-Economic Data Visualization Tool")
st.divider()
st.markdown("""
    <style>
        .icon {
            font-size: 18px;  /* Adjust the size */
            margin-left: -8px; /* Spacing between icon and text */
            margin-right: 8px;
        }
        h2 {
            display: flex;
            align-items: center;
        }
    </style>

    <h2><span class="icon">👀</span> Our Vision</h2>
    <p>Our vision is to leverage socio-economic data for better decision-making and to drive improvements in various sectors such as education, healthcare, and agriculture.</p>

    <h2><span class="icon">❗</span> Problem Statement</h2>
    <p>There is a need for a comprehensive tool that visualizes socio-economic data across different regions to help policymakers and analysts understand trends and patterns.</p>

    <h2><span class="icon">💡</span> Solution</h2>
    <p>Our tool provides an intuitive interface for visualizing state-wise socio-economic data, helping users to make informed decisions based on accurate and timely information.</p>
""", unsafe_allow_html=True)
