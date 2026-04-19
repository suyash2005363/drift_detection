import streamlit as st
import numpy as np
import joblib

st.title("🤖 Prediction Page")

# Load model
model = joblib.load("model.pkl")

st.subheader("Enter Input Features:")

# Example: change according to your dataset
feature1 = st.number_input("Feature 1")
feature2 = st.number_input("Feature 2")
feature3 = st.number_input("Feature 3")

if st.button("Predict"):
    data = np.array([[feature1, feature2, feature3]])
    prediction = model.predict(data)

    st.success(f"Prediction: {prediction[0]}")