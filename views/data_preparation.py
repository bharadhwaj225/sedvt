import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(layout="wide")

st.title("Data Preprocessing, visualization and Model Evaluation")
st.divider()

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/data.csv")
    df = df.dropna()  # Drop rows has no value
    return df

df = load_data()

# Display raw data
st.subheader("📋 Raw Data")
st.write(df)

# Display statistics
st.subheader("📊 Data Statistics")
st.write(df.describe())

# Feature selection for visualization
st.subheader("📈 Data Distributions")
selected_feature = st.selectbox("Select a feature to visualize:", df.columns[1:])
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df[selected_feature], kde=True, bins=20, ax=ax, color="royalblue")
st.pyplot(fig)

# Correlation Heatmap
st.subheader("📌 Feature Correlation Heatmap")
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

# Train-Test Split
st.subheader("⚙️ Data Preprocessing & Model Training")
test_size = st.slider("Select Train-Test Split Ratio:", 0.1, 0.5, 0.2, 0.05)

# Define Features & Target
target_column = "2011-12-INC"  # Define prediction target
X = df.drop(columns=["States_UnionTerritories", target_column])
y = df[target_column]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
st.write(f"✅ Data split completed: {100 * (1-test_size):.0f}% training, {100 * test_size:.0f}% testing.")

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

st.write("✅ Model trained successfully using **Linear Regression**.")

# Feature Importance
st.subheader("🔍 Feature Importance")
feature_importance = pd.DataFrame({"Feature": X.columns, "Importance": model.coef_})
feature_importance = feature_importance.sort_values(by="Importance", ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=feature_importance,
    x="Importance",
    y="Feature",
    palette="coolwarm",
    hue='Feature',
    dodge=False,
    ax=ax,
    legend=False
)
st.pyplot(fig)

# Model Evaluation
st.subheader("📉 Model Evaluation")

# Predictions
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.write(f"🔹 **Mean Squared Error (MSE):** {mse:.2f}")
st.write(f"🔹 **R² Score:** {r2:.4f} (Closer to 1 is better)")

# Predictions vs Actual Values
st.subheader("📊 Predictions vs Actual Values")
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(y_test, y_pred, color="teal", alpha=0.6)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
ax.set_xlabel("Actual Values")
ax.set_ylabel("Predicted Values")
ax.set_title("Actual vs Predicted Income Levels")
st.pyplot(fig)

# Error Distribution
st.subheader("⚠️ Prediction Error Distribution")
errors = y_test - y_pred
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(errors, bins=20, kde=True, color="red", ax=ax)
ax.set_xlabel("Prediction Error")
ax.set_title("Error Distribution")
st.pyplot(fig)
