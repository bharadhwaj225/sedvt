import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/data.csv")

df = load_data()

# Streamlit UI
st.title("State-wise Trend Analysis")

# Dropdown for state selection
selected_state = st.selectbox("Select a state for comparison:", df["States_UnionTerritories"].unique())

st.divider()

# Filter data for selected state
state_data = df[df["States_UnionTerritories"] == selected_state].iloc[0]

# Define all comparison factors
factors = {
    "Income": ("2000-01-INCOME", "2011-12-INCOME"),
    "Literacy Rate": ("2001-LITERACY_RATE", "2011-LITERACY_RATE"),
    "Population": ("2001-POPULATION", "2011-POPULATION"),
    "Sex Ratio": ("2001-SEX_RATIO", "2011-SEX_RATIO"),
    "Unemployment Rate": ("2001-UNEMPLOYMENT_RATE", "2011-UNEMPLOYMENT_RATE"),
    "Poverty Rate": ("2001-POVERTY", "2011-POVERTY")
}

# Function to generate AI insights (limited to 3-4 points)
def generate_insight(factor, value_2001, value_2011, state):
    if not GROQ_API_KEY or not GROQ_API_URL:
        return "⚠️ AI insights unavailable. API credentials missing."

    prompt = f"""
    Analyze the trend of {factor} in {state} from 2001 to 2011.
    The values were {value_2001} in 2001 and {value_2011} in 2011.
    Provide 3 to 4 key points summarizing the change and its possible reasons.
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        insight_text = response.json()["choices"][0]["message"]["content"]
        
        # Extract first 3-4 points
        insights = insight_text.split("\n")
        filtered_insights = [point for point in insights if point.strip()][:4]
        return "\n".join(filtered_insights)

    except requests.exceptions.RequestException as e:
        return f"⚠️ AI insights unavailable. Error: {e}"

# Generate comparisons for each factor
for factor, (year_2001, year_2011) in factors.items():
    value_2001 = state_data[year_2001]
    value_2011 = state_data[year_2011]
    percentage_change = ((value_2011 - value_2001) / value_2001) * 100

    # Display factor title
    st.subheader(f"{factor} Comparison - {selected_state}")

    # Use different visualizations based on factor type
    fig = px.bar(
        x=["2001", "2011"],
        y=[value_2001, value_2011],
        labels={"x": "Year", "y": factor},
        title=f"{factor} Growth",
        color=["2001", "2011"],
        color_discrete_map={"2001": "#4a90e2", "2011": "#ff5733"},
    )
    fig.update_xaxes(type="category")
    fig.update_traces(
        textposition="outside",
        width=0.4,
        hovertemplate=f"{factor}: %{{y}}<extra></extra>"
    )

    # Show graph
    st.plotly_chart(fig)

    # Display percentage change
    st.write(f"📈 **Percentage Change (2001-2011):** {percentage_change:.2f}%")

    # AI-generated insights (limited to 3-4 points)
    with st.spinner("Generating AI insights..."):
        ai_insight = generate_insight(factor, value_2001, value_2011, selected_state)
    st.write(f"🤖 **AI Insight:**\n{ai_insight}")

    st.divider()

# 🔹 AI-powered Overall Performance Analysis
def overall_performance_analysis(state, state_data):
    if not GROQ_API_KEY or not GROQ_API_URL:
        return "⚠️ AI insights unavailable. API credentials missing."

    # Prepare the data summary for AI
    data_summary = "\n".join(
        [f"{factor}: {state_data[year_2001]} (2001) → {state_data[year_2011]} (2011)"
         for factor, (year_2001, year_2011) in factors.items()]
    )

    prompt = f"""
    Analyze the overall performance of {state} from 2001 to 2011 based on the following data:
    {data_summary}
    Provide 3 to 4 key insights about the state's progress, challenges, and significant trends.
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        insight_text = response.json()["choices"][0]["message"]["content"]

        # Extract first 3-4 points
        insights = insight_text.split("\n")
        filtered_insights = [point for point in insights if point.strip()][:4]
        return "\n".join(filtered_insights)

    except requests.exceptions.RequestException as e:
        return f"⚠️ AI insights unavailable. Error: {e}"

# Display AI-powered overall performance analysis
st.subheader(f"📊 Overall Performance Analysis - {selected_state}")

with st.spinner("Analyzing overall state performance..."):
    overall_insights = overall_performance_analysis(selected_state, state_data)

st.write(f"🤖 **AI Summary:**\n{overall_insights}")
