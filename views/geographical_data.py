import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# st.set_page_config(layout="wide")

# State coordinates for mapping
state_coordinates = {
    'Andaman and Nicobar Islands': [11.66702557, 92.73598262],
    'Andhra Pradesh': [15.9129, 79.7400],
    'Arunachal Pradesh': [28.2180, 94.7278],
    'Assam': [26.2006, 92.9376],
    'Bihar': [25.0961, 85.3131],
    'Chandigarh': [30.7333, 76.7794],
    'Chhattisgarh': [21.2787, 81.8661],
    'Delhi': [28.6139, 77.2090],
    'Goa': [15.2993, 74.1240],
    'Gujarat': [22.2587, 71.1924],
    'Haryana': [29.0588, 76.0856],
    'Himachal Pradesh': [31.1048, 77.1734],
    'Jammu and Kashmir': [33.7782, 76.5762],
    'Jharkhand': [23.6102, 85.2799],
    'Karnataka': [15.3173, 75.7139],
    'Kerala': [10.8505, 76.2711],
    'Madhya Pradesh': [22.9734, 78.6569],
    'Maharashtra': [19.7515, 75.7139],
    'Manipur': [24.6637, 93.9063],
    'Meghalaya': [25.4670, 91.3662],
    'Mizoram': [23.1645, 92.9376],
    'Nagaland': [26.1584, 94.5624],
    'Odisha': [20.9517, 85.0985],
    'Puducherry': [11.9416, 79.8083],
    'Punjab': [31.1471, 75.3412],
    'Rajasthan': [27.0238, 74.2179],
    'Sikkim': [27.5330, 88.5122],
    'Tamil Nadu': [11.1271, 78.6569],
    'Tripura': [23.9408, 91.9882],
    'Uttar Pradesh': [26.8467, 80.9462],
    'Uttarakhand': [30.0668, 79.0193],
    'West Bengal': [22.9868, 87.8550]
}

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('data/data.csv')

df = load_data()

# Streamlit app
st.title("Geographic Mapping of Statewise Metrics for 2001 and 2011 📌")
st.divider()

# Display raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(df)

# Function to map a value to a color
def value_to_color(value, min_val, max_val):
    norm_value = (value - min_val) / (max_val - min_val)
    blue = int(255 * (1 - norm_value))
    red = int(255 * norm_value)
    return f"#{red:02x}{0:02x}{blue:02x}"

# Function to create a map for a given column
def create_map(column_name):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    
    min_val = df[column_name].min()
    max_val = df[column_name].max()
    
    for idx, row in df.iterrows():
        location = state_coordinates[row['States_UnionTerritories']]
        value = row[column_name]
        color = value_to_color(value, min_val, max_val)
        
        folium.CircleMarker(
            location=location,
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=f"{row['States_UnionTerritories']}<br>{column_name}: {value}"
        ).add_to(m)
    
    return m

# Create maps for selected columns
columns_to_map = ['2011-12-INC', '2011-LIT', '2011-POP', '2011-SEX_RATIO', '2011-UNEMP', '2011-Poverty']
for col in columns_to_map:
    st.subheader(f"Geographic Mapping for {col}")
    m = create_map(col)
    st_folium(m, width=700, height=500)
