import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os

st.title("🤖 Income Prediction")

# -------------------------------
# LOAD MODEL FILES
# -------------------------------

base_dir = os.path.dirname(os.path.dirname(__file__))

model = joblib.load(os.path.join(base_dir, "Models", "model.pkl"))
scaler = joblib.load(os.path.join(base_dir, "Models", "scaler.pkl"))
lda = joblib.load(os.path.join(base_dir, "Models", "lda.pkl"))

# -------------------------------
# INPUT UI
# -------------------------------

st.subheader("Enter Details")

age = st.number_input("Age", min_value=17, max_value=90, value=30)

workclass = st.selectbox("Workclass", [
    "Private", "Self-emp-not-inc", "State-gov", "Federal-gov"
])

fnlwgt = st.number_input("fnlwgt", value=100000)

education = st.selectbox("Education", [
    "Bachelors", "HS-grad", "Masters"
])

education_num = st.number_input("Education Number", value=10)

marital_status = st.selectbox("Marital Status", [
    "Never-married", "Married", "Divorced"
])

occupation = st.selectbox("Occupation", [
    "Tech-support", "Craft-repair", "Sales", "Exec-managerial"
])

relationship = st.selectbox("Relationship", [
    "Not-in-family", "Husband", "Wife"
])

race = st.selectbox("Race", [
    "White", "Black", "Asian-Pac-Islander"
])

sex = st.selectbox("Sex", ["Male", "Female"])

capital_gain = st.number_input("Capital Gain", value=0)
capital_loss = st.number_input("Capital Loss", value=0)

hours_per_week = st.number_input("Hours per Week", value=40)

native_country = st.selectbox("Native Country", [
    "United-States", "India", "Canada"
])

# -------------------------------
# MANUAL ENCODING
# -------------------------------

workclass_map = {
    "Private": 0, "Self-emp-not-inc": 1, "State-gov": 2, "Federal-gov": 3
}

education_map = {
    "Bachelors": 0, "HS-grad": 1, "Masters": 2
}

marital_map = {
    "Never-married": 0, "Married": 1, "Divorced": 2
}

occupation_map = {
    "Tech-support": 0, "Craft-repair": 1, "Sales": 2, "Exec-managerial": 3
}

relationship_map = {
    "Not-in-family": 0, "Husband": 1, "Wife": 2
}

race_map = {
    "White": 0, "Black": 1, "Asian-Pac-Islander": 2
}

sex_map = {
    "Male": 0, "Female": 1
}

country_map = {
    "United-States": 0, "India": 1, "Canada": 2
}

# -------------------------------
# PREDICTION
# -------------------------------

if st.button("Predict"):

    # Create DataFrame (FIXES WARNING)
    input_dict = {
        "age": age,
        "workclass": workclass_map[workclass],
        "fnlwgt": fnlwgt,
        "education": education_map[education],
        "education.num": education_num,
        "marital.status": marital_map[marital_status],
        "occupation": occupation_map[occupation],
        "relationship": relationship_map[relationship],
        "race": race_map[race],
        "sex": sex_map[sex],
        "capital.gain": capital_gain,
        "capital.loss": capital_loss,
        "hours.per.week": hours_per_week,
        "native.country": country_map[native_country]
    }

    input_df = pd.DataFrame([input_dict])

    try:
        # Apply full pipeline
        scaled = scaler.transform(input_df)
        transformed = lda.transform(scaled)
        prediction = model.predict(transformed)

        if prediction[0] == 1:
            st.success("💰 Income > 50K")
        else:
            st.success("📉 Income <= 50K")

    except Exception as e:
        st.error(f"Error: {e}")