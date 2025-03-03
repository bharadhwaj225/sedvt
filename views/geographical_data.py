import streamlit as st
import pandas as pd
import folium
import requests
import os
from dotenv import load_dotenv
from streamlit_folium import st_folium

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

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

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv('data/data.csv')

df = load_data()

# Function to get temperature
@st.cache_data(ttl=3600)
def get_temperature(lat, lon):
    """Fetch temperature data with caching."""
    if not API_KEY:
        return "API Key Missing"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return round(data["main"]["temp"], 1)
    except requests.exceptions.RequestException:
        return "N/A"

# Function to map value to color
def value_to_color(value, min_val, max_val):
    norm_value = (value - min_val) / (max_val - min_val)
    blue = int(255 * (1 - norm_value))
    red = int(255 * norm_value)
    return f"#{red:02x}{0:02x}{blue:02x}"

# Function to create folium map
def create_map(column_name):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB positron")  # Fast tiles
    
    min_val = df[column_name].min()
    max_val = df[column_name].max()

    for idx, row in df.iterrows():
        state = row['States_UnionTerritories']
        location = state_coordinates.get(state)

        if location:
            value = row[column_name]
            color = value_to_color(value, min_val, max_val)
            temp = get_temperature(location[0], location[1])

            # Tooltip with temperature
            tooltip_text = f"{state}<br>{column_name}: {value}<br>🌡 Temperature: {temp}°C" if temp != "N/A" else f"{state}<br>{column_name}: {value}<br>🌡 Temperature: Not Available"

            folium.CircleMarker(
                location=location,
                radius=10,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                tooltip=tooltip_text
            ).add_to(m)

    return m

# Streamlit UI
st.title("Geographic Mapping of Statewise Metrics")
st.divider()

# Show raw data checkbox
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(df)

# Select data column for mapping
columns_to_map = ['2011-12-INCOME', '2011-LITERACY_RATE', '2011-POPULATION', '2011-SEX_RATIO', '2011-UNEMPLOYMENT_RATE', '2011-POVERTY']
selected_column = st.selectbox("Select Data to Map", columns_to_map)

# Display folium map
st.subheader(f"Geographic Mapping for {selected_column}")
m = create_map(selected_column)
st_folium(m, width=700, height=500)
