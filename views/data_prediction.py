import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import IsolationForest

st.set_page_config(layout="wide")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('data/data.csv')
    df = df.dropna()  
    return df

df = load_data()

st.title("📈 Poverty Rate Prediction & Fraud Detection")
st.divider()

# Data Overview
st.subheader("📋 Data Overview")
st.write(df.head())

# Improved Bar Chart using Plotly
st.subheader("📊 Poverty Data for 2001 and 2011")
fig = px.bar(df, x='States_UnionTerritories', y=['2001-POVERTY', '2011-POVERTY'],
             barmode='group', labels={'value': 'Poverty Rate (%)'}, title="Poverty Rates Over the Years")
st.plotly_chart(fig)

# Improved Feature Correlation with Seaborn Heatmap
st.subheader("🔍 Correlation Matrix")
fig, ax = plt.subplots(figsize=(8, 6))
numeric_df = df.select_dtypes(include=[np.number])  # Select only numeric columns
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)

st.pyplot(fig)

# Model Training
st.subheader("🤖 Predictive Analytics")

# Feature Selection & Scaling
features_2021 = ['2001-POVERTY', '2011-POVERTY', '2011-LITERACY_RATE', '2011-UNEMPLOYMENT_RATE']
X_2021 = df[features_2021]
y_2021 = df['2011-POVERTY']

scaler = StandardScaler()
X_2021_scaled = scaler.fit_transform(X_2021)

X_train_2021, X_test_2021, y_train_2021, y_test_2021 = train_test_split(X_2021_scaled, y_2021, test_size=0.2, random_state=42)

# Compare Linear Regression & RandomForest
model_2021_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_2021_rf.fit(X_train_2021, y_train_2021)

df['Predicted 2021-POVERTY'] = model_2021_rf.predict(X_2021_scaled)

# Train Model for 2031
features_2031 = ['2001-POVERTY', '2011-POVERTY', 'Predicted 2021-POVERTY', '2011-LITERACY_RATE', '2011-UNEMPLOYMENT_RATE']
X_2031 = df[features_2031]
scaler_2031 = StandardScaler()
X_2031_scaled = scaler_2031.fit_transform(X_2031)


X_train_2031, X_test_2031, y_train_2031, y_test_2031 = train_test_split(X_2031_scaled, y_2021, test_size=0.2, random_state=42)

model_2031_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_2031_rf.fit(X_train_2031, y_train_2031)

df['Predicted 2031-POVERTY'] = model_2031_rf.predict(X_2031_scaled)

st.write(df[['States_UnionTerritories', 'Predicted 2021-POVERTY', 'Predicted 2031-POVERTY']])

# Model Performance
y_pred_2021 = model_2021_rf.predict(X_test_2021)
y_pred_2031 = model_2031_rf.predict(X_test_2031)

st.write(f"✅ **Model Performance for 2021 Prediction:**")
st.write(f"🔹 **MSE:** {mean_squared_error(y_test_2021, y_pred_2021):.2f}, **R² Score:** {r2_score(y_test_2021, y_pred_2021):.4f}")

st.write(f"✅ **Model Performance for 2031 Prediction:**")
st.write(f"🔹 **MSE:** {mean_squared_error(y_test_2031, y_pred_2031):.2f}, **R² Score:** {r2_score(y_test_2031, y_pred_2031):.4f}")

# Fraud Detection with Isolation Forest
st.subheader("⚠️ Fraud Detection - Unusual Poverty Rates")
iso_forest = IsolationForest(contamination=0.1, random_state=42)
df["Anomaly"] = iso_forest.fit_predict(df[['2011-POVERTY']])
anomalies = df[df["Anomaly"] == -1]

fig = px.box(df, y='2011-POVERTY', title="Poverty Rate Distribution with Outliers")
st.plotly_chart(fig)

if not anomalies.empty:
    st.warning("🚨 Possible fraud detected in these states:")
    st.write(anomalies[['States_UnionTerritories', '2011-POVERTY']])

st.divider()

# Custom Prediction UI
st.subheader("🔮 Custom Prediction")

use_dataset = st.checkbox("Use dataset values for prediction")

if use_dataset:
    state_selected = st.selectbox("Select State/UT:", df["States_UnionTerritories"])
    selected_row = df[df["States_UnionTerritories"] == state_selected].iloc[0]
    poverty_2001 = selected_row["2001-POVERTY"]
    poverty_2011 = selected_row["2011-POVERTY"]
    literacy_2011 = selected_row["2011-LITERACY_RATE"]
    unemployment_2011 = selected_row["2011-UNEMPLOYMENT_RATE"]
else:
    poverty_2001 = st.slider("2001 Poverty Rate:", 0.0, 100.0, 20.0)
    poverty_2011 = st.slider("2011 Poverty Rate:", 0.0, 100.0, 18.0)
    literacy_2011 = st.slider("2011 Literacy Rate:", 0.0, 100.0, 70.0)
    unemployment_2011 = st.slider("2011 Unemployment Rate:", 0.0, 100.0, 5.0)

input_data_2021 = pd.DataFrame([[poverty_2001, poverty_2011, literacy_2011, unemployment_2011]], 
                               columns=features_2021)
input_data_2021_scaled = scaler.transform(input_data_2021)
predicted_2021 = model_2021_rf.predict(input_data_2021_scaled)

input_data_2031 = pd.DataFrame([[poverty_2001, poverty_2011, predicted_2021[0], literacy_2011, unemployment_2011]], 
                               columns=features_2031)
input_data_2031_scaled = scaler_2031.transform(input_data_2031)
predicted_2031 = model_2031_rf.predict(input_data_2031_scaled)

if st.button("Predict"):
    st.success(f"🔹 **Predicted 2021 Poverty Rate:** {predicted_2021[0]:.2f}%")
    st.success(f"🔹 **Predicted 2031 Poverty Rate:** {predicted_2031[0]:.2f}%")
