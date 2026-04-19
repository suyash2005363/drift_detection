import streamlit as st
import numpy as np
import joblib
import os

st.title("🤖 Income Prediction")

# Get base path
base_dir = os.path.dirname(os.path.dirname(__file__))

# Load files
model = joblib.load(os.path.join(base_dir, "Models", "model.pkl"))
scaler = joblib.load(os.path.join(base_dir, "Models", "scaler.pkl"))
lda = joblib.load(os.path.join(base_dir, "Models", "lda.pkl"))
features = joblib.load(os.path.join(base_dir, "Models", "features.pkl"))

st.subheader("Enter Input Features")

# Input fields
input_data = []

for feature in features:
    value = st.number_input(f"{feature}", value=0.0)
    input_data.append(value)

if st.button("Predict"):
    data = np.array([input_data])

    try:
        data_scaled = scaler.transform(data)
        data_lda = lda.transform(data_scaled)
        prediction = model.predict(data_lda)

        if prediction[0] == 1:
            st.success("Income > 50K")
        else:
            st.success("Income <= 50K")

    except Exception as e:
        st.error(f"Error: {e}")