import streamlit as st
import pandas as pd
import plotly.express as px
import uuid  # Ensure unique keys

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/data.csv")

df = load_data()

# Streamlit UI
st.title("State-wise Comparison Tool")

# Dropdowns for selecting two states (No default selection)
col1, spacer, col2 = st.columns([1, 0.5, 1])  # Adjusted spacing
with col1:
    state_1 = st.selectbox("Select First State:", [""] + list(df["States_UnionTerritories"].unique()), index=0)
with col2:
    state_2 = st.selectbox("Select Second State:", [""] + list(df["States_UnionTerritories"].unique()), index=0)

# Placeholder text that updates dynamically
text_placeholder = st.empty()
if not state_1 or not state_2:
    text_placeholder.info("Please select two states for comparison.")
elif state_1 == state_2:
    text_placeholder.error("Please select two different states for comparison.")
else:
    text_placeholder.success(f"Comparing **{state_1}** and **{state_2}** across multiple factors.")

    # Filter data for selected states
    data_1 = df[df["States_UnionTerritories"] == state_1].iloc[0]
    data_2 = df[df["States_UnionTerritories"] == state_2].iloc[0]

    # Define comparison factors
    factors = {
        "Income": ("2000-01-INCOME", "2011-12-INCOME"),
        "Literacy Rate": ("2001-LITERACY_RATE", "2011-LITERACY_RATE"),
        "Population": ("2001-POPULATION", "2011-POPULATION"),
        "Sex Ratio": ("2001-SEX_RATIO", "2011-SEX_RATIO"),
        "Unemployment Rate": ("2001-UNEMPLOYMENT_RATE", "2011-UNEMPLOYMENT_RATE"),
        "Poverty Rate": ("2001-POVERTY", "2011-POVERTY")
    }

    # Display factors with proper spacing
    for factor, (year_2001, year_2011) in factors.items():
        col1, spacer, col2 = st.columns([1, 0.5, 1])  # Add spacing column

        with col1:
            y_values_1 = [data_1[year_2001], data_1[year_2011]]
            hover_template_1 = (
                f"{factor}: %{{y}} in thousands<extra></extra>"
                if factor == "Population"
                else f"{factor}: %{{y}}<extra></extra>"
            )

            fig1 = px.bar(
                x=["2001", "2011"],
                y=y_values_1,
                labels={"x": "Year", "y": factor},
                title=f"{factor} - {state_1}",
                color=["2001", "2011"],
                color_discrete_map={"2001": "#4a90e2", "2011": "#ff5733"},
                text=y_values_1
            )
            fig1.update_xaxes(type="category")
            fig1.update_traces(
                textposition="outside",
                width=0.4,
                hovertemplate=hover_template_1
            )
            st.plotly_chart(fig1, use_container_width=True, key=f"{state_1}_{factor}_{uuid.uuid4().hex}")

        with col2:
            y_values_2 = [data_2[year_2001], data_2[year_2011]]
            hover_template_2 = (
                f"{factor}: %{{y}} in thousands<extra></extra>"
                if factor == "Population"
                else f"{factor}: %{{y}}<extra></extra>"
            )

            fig2 = px.bar(
                x=["2001", "2011"],
                y=y_values_2,
                labels={"x": "Year", "y": factor},
                title=f"{factor} - {state_2}",
                color=["2001", "2011"],
                color_discrete_map={"2001": "#4a90e2", "2011": "#ff5733"},
                text=y_values_2
            )
            fig2.update_xaxes(type="category")
            fig2.update_traces(
                textposition="outside",
                width=0.4,
                hovertemplate=hover_template_2
            )
            st.plotly_chart(fig2, use_container_width=True, key=f"{state_2}_{factor}_{uuid.uuid4().hex}")

    # Side-by-Side Table Comparison
    st.subheader("📋 Data Table Comparison")

    comparison_data = {
        "Factor": list(factors.keys()),
        f"{state_1} (2001)": [data_1[factors[f][0]] for f in factors],
        f"{state_1} (2011)": [data_1[factors[f][1]] for f in factors],
        f"{state_2} (2001)": [data_2[factors[f][0]] for f in factors],
        f"{state_2} (2011)": [data_2[factors[f][1]] for f in factors],
    }

    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df)
