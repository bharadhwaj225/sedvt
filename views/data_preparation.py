import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(layout="wide")

st.title("Socio-Economic Data Analysis & Predictive Model Evaluation")
st.divider()

st.markdown("""
### Overview
In our AI-Powered Socio-Economic Data Visualization and Predictive Analytics Tool, data preprocessing is a critical step. 
We clean, transform, and analyze socio-economic data to derive actionable insights and predict key indicators like income levels. 
Below, you can explore the steps involved in preprocessing, visualizing, and evaluating our predictive model for the '2011-12-INCOME' indicator.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("data/data.csv")
    df = df.dropna()
    return df

df = load_data()

st.subheader("📋 Raw Data Preview")
st.write(df.head(10))


st.subheader("📊 Data Summary Statistics")
st.write(df.describe())

# Data Distribution Visualization
st.markdown("### Data Distributions")
selected_feature = st.selectbox("Select a feature for distribution analysis:", df.columns[1:])
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df[selected_feature], kde=True, bins=20, ax=ax, color="royalblue")
ax.set_title(f"Distribution of {selected_feature}", fontsize=14)
st.pyplot(fig)

# Correlation Heatmap for feature interactions
st.markdown("### Feature Correlation Analysis")
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title("Correlation Heatmap of Numeric Features", fontsize=14)
st.pyplot(fig)

# Data Preprocessing and Model Training
st.markdown("### Data Preprocessing & Predictive Model Training")
st.markdown("""
In this section, we split the data for model training and testing, then build a predictive model using Linear Regression 
to forecast '2011-12-INCOME' levels. This model serves as a preliminary step in our larger predictive analytics framework.
""")

# Slider to select the Train-Test split ratio
test_size = st.slider("Select Train-Test Split Ratio:", 0.1, 0.5, 0.2, 0.05)

target_column = "2011-12-INCOME"  # Income as the socio-economic indicator to predict
X = df.drop(columns=["States_UnionTerritories", target_column])
y = df[target_column]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
st.write(f"✅ Data split completed: {100 * (1-test_size):.0f}% training data and {100 * test_size:.0f}% testing data.")

model = LinearRegression()
model.fit(X_train, y_train)
st.write("✅ Linear Regression model trained successfully for predicting income levels.")

st.markdown("### 🔍 Feature Importance Analysis")
feature_importance = pd.DataFrame({"Feature": X.columns, "Importance": model.coef_})
feature_importance = feature_importance.sort_values(by="Importance", ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=feature_importance, x="Importance", y="Feature", hue="Feature", palette="coolwarm", legend=False, ax=ax)
ax.set_title("Feature Importance in Income Prediction", fontsize=14)
st.pyplot(fig)

st.markdown("### 📉 Model Evaluation Metrics")
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.write(f"🔹 **Mean Squared Error (MSE):** {mse:.2f}")
st.write(f"🔹 **R² Score:** {r2:.4f} (Closer to 1 indicates better performance)")

st.markdown("### 📊 Actual vs. Predicted Income Levels")
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(y_test, y_pred, color="teal", alpha=0.6)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
ax.set_xlabel("Actual Income Levels")
ax.set_ylabel("Predicted Income Levels")
ax.set_title("Comparison of Actual and Predicted Income", fontsize=14)
st.pyplot(fig)

# Error Distribution Visualization
st.markdown("### ⚠️ Distribution of Prediction Errors")
errors = y_test - y_pred
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(errors, bins=20, kde=True, color="red", ax=ax)
ax.set_xlabel("Prediction Error")
ax.set_title("Error Distribution in Income Prediction", fontsize=14)
st.pyplot(fig)

st.markdown("""
---
### Summary
This section detailed the complete workflow for data preprocessing, visualization, and predictive model evaluation for our socio-economic dataset. 
By cleaning and exploring the data, training a Linear Regression model, and evaluating its performance, we have laid the groundwork for advanced predictive analytics that will further enhance our AI-powered Socio-Economic Data Visualization and Predictive Analytics Tool.
""")
