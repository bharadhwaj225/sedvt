import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import io

# Load CSV with error handling
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/data.csv")
        df = df.dropna()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Check if data loaded successfully
if df.empty:
    st.error("No data available. Please check the CSV file.")
    st.stop()

st.title("Interactive Dashboard: Indian States Data")
st.markdown("This dashboard displays various socio-economic metrics for Indian states and union territories from different years.")

# Get list of states and numeric metrics (excluding the state column)
states = df["States_UnionTerritories"].unique().tolist()
numeric_metrics = [col for col in df.columns if col != "States_UnionTerritories"]

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "Scatter Plot",
    "Line Charts",
    "Data Summary"
])

# Tab 1: Dashboard – Filters, Bar Chart & Pie Chart

with tab1:
    st.header("Dashboard: Filters, Bar Chart & Population Pie Chart")
    # Filter for states
    selected_states = st.multiselect("Select States/Union Territories", options=states, default=states, key="tab1_states")
    filtered_df = df[df["States_UnionTerritories"].isin(selected_states)]
    
    # Option to download filtered data
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data", data=csv, file_name="filtered_data.csv", mime="text/csv")
    
    # Bar chart for selected metric
    metric = st.selectbox("Select metric for Bar Chart", options=numeric_metrics, key="bar_metric")
    bar_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("States_UnionTerritories:N", title="State/Union Territory", sort="-y"),
        y=alt.Y(f"{metric}:Q", title=metric),
        tooltip=["States_UnionTerritories", metric]
    ).properties(width=700, height=400, title=f"{metric} across States/UTs")
    st.altair_chart(bar_chart, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Population Pie Chart")
    # Pie chart for population data
    population_col = st.selectbox("Select Population Year", options=["2001-POPULATION", "2011-POPULATION"], key="pop_year")
    pie_chart = alt.Chart(filtered_df).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field=population_col, type="quantitative", title="Population"),
        color=alt.Color(field="States_UnionTerritories", type="nominal", legend=alt.Legend(title="State/UT")),
        tooltip=["States_UnionTerritories", population_col]
    ).properties(width=700, height=400, title="Population Distribution")
    st.altair_chart(pie_chart, use_container_width=True)


# Tab 2: Scatter Plot – Compare any two metrics
with tab2:
    st.header("Scatter Plot: Compare Two Metrics")
    selected_states_scatter = st.multiselect("Select States/Union Territories", options=states, default=states, key="tab2_states")
    scatter_df = df[df["States_UnionTerritories"].isin(selected_states_scatter)]
    
    x_metric = st.selectbox("Select X-axis Metric", options=numeric_metrics, key="x_metric")
    y_metric = st.selectbox("Select Y-axis Metric", options=numeric_metrics, key="y_metric")
    
    scatter_chart = alt.Chart(scatter_df).mark_circle(size=100).encode(
        x=alt.X(x_metric, title=x_metric),
        y=alt.Y(y_metric, title=y_metric),
        color="States_UnionTerritories:N",
        tooltip=["States_UnionTerritories", x_metric, y_metric]
    ).properties(width=700, height=400, title=f"{x_metric} vs {y_metric}")
    st.altair_chart(scatter_chart, use_container_width=True)

# Tab 3: Line Charts – Unemployment & Income Comparison

with tab3:
    st.header("Line Charts: Unemployment & Income Comparison")
    selected_states_line = st.multiselect("Select States/Union Territories", options=states, default=states, key="tab3_states")
    line_df = df[df["States_UnionTerritories"].isin(selected_states_line)]
    
    # Unemployment Comparison
    st.subheader("Unemployment Rates Comparison (2001 vs 2011)")
    unemployment_cols = ["2001-UNEMPLOYMENT_RATE", "2011-UNEMPLOYMENT_RATE"]
    if all(col in df.columns for col in unemployment_cols):
        unemployment_long = line_df.melt(
            id_vars=["States_UnionTerritories"],
            value_vars=unemployment_cols,
            var_name="Year",
            value_name="Unemployment Rate"
        )
        unemployment_chart = alt.Chart(unemployment_long).mark_line(point=True).encode(
            x=alt.X("Year:N", title="Year"),
            y=alt.Y("Unemployment Rate:Q", title="Unemployment Rate"),
            color="States_UnionTerritories:N",
            tooltip=["States_UnionTerritories", "Year", "Unemployment Rate"]
        ).properties(width=700, height=400, title="Unemployment Rate Trend")
        st.altair_chart(unemployment_chart, use_container_width=True)
    else:
        st.info("Unemployment columns not found in data.")

    st.markdown("---")
    # Income Comparison
    st.subheader("Income Comparison (2000-01 vs 2011-12)")
    income_cols = ["2000-01-INCOME", "2011-12-INCOME"]
    if all(col in df.columns for col in income_cols):
        income_long = line_df.melt(
            id_vars=["States_UnionTerritories"],
            value_vars=income_cols,
            var_name="Year",
            value_name="Income"
        )
        income_chart = alt.Chart(income_long).mark_line(point=True).encode(
            x=alt.X("Year:N", title="Year"),
            y=alt.Y("Income:Q", title="Income"),
            color="States_UnionTerritories:N",
            tooltip=["States_UnionTerritories", "Year", "Income"]
        ).properties(width=700, height=400, title="Income Trend Comparison")
        st.altair_chart(income_chart, use_container_width=True)
    else:
        st.info("Income columns not found in data.")

# Tab 4: Data Summary – Summary Statistics & Correlation Heatmap

with tab4:
    st.header("Data Summary: Statistics & Correlation Heatmap")
    selected_states_summary = st.multiselect("Select States/Union Territories", options=states, default=states, key="tab4_states")
    summary_df = df[df["States_UnionTerritories"].isin(selected_states_summary)]
    
    st.subheader("Summary Statistics")
    st.dataframe(summary_df[numeric_metrics].describe())
    
    st.subheader("Correlation Heatmap")
    corr = summary_df[numeric_metrics].corr().reset_index().melt(id_vars='index')
    corr.columns = ['Metric 1', 'Metric 2', 'Correlation']
    heatmap = alt.Chart(corr).mark_rect().encode(
        x=alt.X("Metric 1:N", title="Metric"),
        y=alt.Y("Metric 2:N", title="Metric"),
        color=alt.Color("Correlation:Q", scale=alt.Scale(scheme="viridis")),
        tooltip=["Metric 1", "Metric 2", "Correlation"]
    ).properties(width=700, height=600, title="Correlation Heatmap of Selected Metrics")
    st.altair_chart(heatmap, use_container_width=True)
