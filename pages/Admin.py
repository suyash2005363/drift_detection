import streamlit as st
import pandas as pd
from drift import detect_drift  # make sure this function exists

st.title("🔐 Admin Panel - Drift Monitoring")

# Hardcoded login
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username == "admin" and password == "admin123":
    st.success("Login Successful!")

    st.subheader("📊 Drift Detection")

    # Example: Load your datasets
    reference = pd.read_csv("reference_predictions.csv")
    current = pd.read_csv("reference_batch_errors.csv")

    if st.button("Run Drift Detection"):
        result = detect_drift(reference, current)

        st.write("### Drift Result:")
        st.write(result)

else:
    st.warning("Enter correct admin credentials")