import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(layout="wide")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('data/data.csv')
    df = df.dropna()  # Drop rows has no value
    return df

df = load_data()

st.title("Poverty Rate Prediction & Fraud Detection")
st.divider()

# Data Visualization
st.subheader("📋 Data Overview")
st.write(df)

st.subheader("📊 Poverty Data for 2001 and 2011")
fig, ax = plt.subplots(figsize=(10, 5))
df.set_index('States_UnionTerritories')[['2001-Poverty', '2011-Poverty']].plot(kind='bar', ax=ax, color=['blue', 'red'])
ax.set_ylabel("Poverty Rate (%)")
st.pyplot(fig)

# Feature Correlation
st.subheader("🔍 Relationship Between Poverty & Other Socio-Economic Factors")
features = ['2001-LIT', '2011-LIT', '2001-UNEMP', '2011-UNEMP']
for feature in features:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df, x=feature, y='2011-Poverty', ax=ax, color="teal")
    ax.set_title(f"{feature} vs 2011 Poverty Rate")
    st.pyplot(fig)

# Model Training for Future Predictions
st.subheader("🤖 Predictive Analytics")
st.write("🔹 Training models to predict **2021 & 2031 Poverty Rates**")

# Train Model for 2021
X_2021 = df[['2001-Poverty', '2011-Poverty', '2011-LIT', '2011-UNEMP']]
y_2021 = df['2011-Poverty']

X_train_2021, X_test_2021, y_train_2021, y_test_2021 = train_test_split(X_2021, y_2021, test_size=0.2, random_state=42)

model_2021 = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model_2021.fit(X_train_2021, y_train_2021)

df['Predicted 2021-Poverty'] = model_2021.predict(X_2021)

# Train Model for 2031 using 2021 Predictions
X_2031 = df[['2001-Poverty', '2011-Poverty', 'Predicted 2021-Poverty', '2011-LIT', '2011-UNEMP']]
y_2031 = df['2011-Poverty']  # Using 2011 as a proxy for training (since we don't have 2021 actuals)

X_train_2031, X_test_2031, y_train_2031, y_test_2031 = train_test_split(X_2031, y_2031, test_size=0.2, random_state=42)

model_2031 = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model_2031.fit(X_train_2031, y_train_2031)

df['Predicted 2031-Poverty'] = model_2031.predict(X_2031)

# st.write(df[['States_UnionTerritories', 'Predicted 2021-Poverty', 'Predicted 2031-Poverty']])
st.write(df[['States_UnionTerritories', 'Predicted 2021-Poverty']])

# Model Performance
y_pred_2021 = model_2021.predict(X_test_2021)
y_pred_2031 = model_2031.predict(X_test_2031)

mse_2021 = mean_squared_error(y_test_2021, y_pred_2021)
r2_2021 = r2_score(y_test_2021, y_pred_2021)

mse_2031 = mean_squared_error(y_test_2031, y_pred_2031)
r2_2031 = r2_score(y_test_2031, y_pred_2031)

st.write(f"✅ **Model Performance for 2021 Prediction:**")
st.write(f"🔹 **MSE:** {mse_2021:.2f}, **R² Score:** {r2_2021:.4f}")

st.write(f"✅ **Model Performance for 2031 Prediction:**")
st.write(f"🔹 **MSE:** {mse_2031:.2f}, **R² Score:** {r2_2031:.4f}")

# Fraud Detection (Anomalies in Poverty Rates)
st.subheader("⚠️ Fraud Detection - Unusual Poverty Rates")
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(df['2011-Poverty'], ax=ax, color="red")
ax.set_title("Poverty Rate Distribution (2011)")
st.pyplot(fig)
st.divider()

# Custom Prediction
st.subheader("Custom Prediction (2021 & 2031)")

use_dataset = st.checkbox("Use dataset values for prediction")

if use_dataset:
    state_selected = st.selectbox("Select State/UT:", df["States_UnionTerritories"])
    selected_row = df[df["States_UnionTerritories"] == state_selected].iloc[0]
    poverty_2001 = selected_row["2001-Poverty"]
    poverty_2011 = selected_row["2011-Poverty"]
    literacy_2011 = selected_row["2011-LIT"]
    unemployment_2011 = selected_row["2011-UNEMP"]
else:
    poverty_2001 = st.number_input("Enter 2001 Poverty Rate:", value=20.0, min_value=0.0, max_value=100.0)
    poverty_2011 = st.number_input("Enter 2011 Poverty Rate:", value=18.0, min_value=0.0, max_value=100.0)
    literacy_2011 = st.number_input("Enter 2011 Literacy Rate:", value=70.0, min_value=0.0, max_value=100.0)
    unemployment_2011 = st.number_input("Enter 2011 Unemployment Rate:", value=5.0, min_value=0.0, max_value=100.0)

# input_data_2021 = np.array([[poverty_2001, poverty_2011, literacy_2011, unemployment_2011]])
input_data_2021 = pd.DataFrame([[poverty_2001, poverty_2011, literacy_2011, unemployment_2011]], columns=['2001-Poverty', '2011-Poverty', '2011-LIT', '2011-UNEMP'])
predicted_2021 = model_2021.predict(input_data_2021)

# input_data_2031 = np.array([[poverty_2001, poverty_2011, predicted_2021[0], literacy_2011, unemployment_2011]])
input_data_2031 = pd.DataFrame([[poverty_2001, poverty_2011, predicted_2021[0], literacy_2011, unemployment_2011]], columns=['2001-Poverty', '2011-Poverty', 'Predicted 2021-Poverty', '2011-LIT', '2011-UNEMP'])
predicted_2031 = model_2031.predict(input_data_2031)

if st.button("Predict"):
    st.write(f"🔹 **Predicted 2021 Poverty Rate:** {predicted_2021[0]:.2f}%")
    st.write(f"🔹 **Predicted 2031 Poverty Rate:** {predicted_2031[0]:.2f}%")
