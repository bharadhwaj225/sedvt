import streamlit as st
import pandas as pd
import plotly.express as px

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

# Generate comparisons for each factor
for factor, (year_2001, year_2011) in factors.items():
    value_2001 = state_data[year_2001]
    value_2011 = state_data[year_2011]
    percentage_change = ((value_2011 - value_2001) / value_2001) * 100

    # Display factor title
    st.subheader(f"{factor} Comparison - {selected_state}")

    # Use different visualizations based on factor type
    if factor in ["Income", "Sex Ratio"]:
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



    elif factor == "Population":
        fig = px.bar(
            x=["2001", "2011"],
            y=[value_2001, value_2011],
            labels={"x": "Year", "y": "Population"},
            title="Population Growth",
            color=["2001", "2011"],
            color_discrete_map={"2001": "#4a90e2", "2011": "#ff5733"},
        )
        fig.update_xaxes(type="category")
        fig.update_traces(
            textposition="outside",
            width=0.4,
            hovertemplate=f"Population: %{{y}} (in thousands)<extra></extra>"
        )

    elif factor == "Literacy Rate":
        fig = px.line(
            x=["2001", "2011"],
            y=[value_2001, value_2011],
            markers=True,
            labels={"x": "Year", "y": factor},
            title=f"{factor} Trend",
            line_shape="linear"
        )
        fig.update_traces(hovertemplate=f"{factor}: %{{y}}%<extra></extra>")

    else:
        fig = px.scatter(
            x=["2001", "2011"],
            y=[value_2001, value_2011],
            size=[value_2001, value_2011],
            labels={"x": "Year", "y": factor},
            title=f"{factor} Analysis",
            color=["2001", "2011"],
            color_discrete_map={"2001": "#4a90e2", "2011": "#ff5733"},
        )
        fig.update_traces(hovertemplate=f"{factor}: %{{y}}<extra></extra>")

    # Show graph
    st.plotly_chart(fig)

    # Display percentage change
    st.write(f"📈 **Percentage Change (2001-2011):** {percentage_change:.2f}%")
    
    st.divider()
