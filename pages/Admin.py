import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

from src.drift.drift_detector import DriftDetector

st.set_page_config(page_title="Drift Monitoring", layout="wide")

st.title("📊 Drift Monitoring Dashboard")

# -------------------------------
# LOGIN
# -------------------------------

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username == "admin" and password == "admin123":

    st.success("✅ Logged in as Admin")

    # -------------------------------
    # LOAD DATA
    # -------------------------------

    base_dir = os.path.dirname(os.path.dirname(__file__))

    reference_path = os.path.join(base_dir, "data", "reference", "reference_dataset.csv")

    batch_file = st.selectbox(
        "📁 Select Current Batch",
        ["batch_1.csv", "batch_2.csv", "batch_3.csv"]
    )

    current_path = os.path.join(base_dir, "data", "income", batch_file)

    reference = pd.read_csv(reference_path)
    current = pd.read_csv(current_path)

    col1, col2 = st.columns(2)
    col1.metric("Reference Rows", reference.shape[0])
    col2.metric("Current Rows", current.shape[0])

    st.divider()

    # -------------------------------
    # RUN DRIFT
    # -------------------------------

    if st.button("🚀 Run Drift Detection"):

        detector = DriftDetector()
        result = detector.detect_drift(reference, current)

        report_data = []

        for feature, details in result.items():
            if "p_value" in details:
                report_data.append({
                    "Feature": feature,
                    "P-Value": round(details["p_value"], 5),
                    "Drift": "Yes" if details["drift_detected"] else "No"
                })

        report_df = pd.DataFrame(report_data)

        # -------------------------------
        # SUMMARY
        # -------------------------------

        total_features = len(report_df)
        drift_count = (report_df["Drift"] == "Yes").sum()
        drift_percent = (drift_count / total_features) * 100

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Features", total_features)
        col2.metric("Drifted Features", drift_count)
        col3.metric("Drift %", f"{drift_percent:.2f}%")

        if drift_count > 0:
            st.error(f"⚠️ Drift detected in {drift_count} features!")
        else:
            st.success("✅ No drift detected")

        st.divider()

        # -------------------------------
        # TABLE WITH HIGHLIGHT
        # -------------------------------

        def highlight_drift(row):
            if row["Drift"] == "Yes":
                return ["background-color: #ffcccc"] * len(row)
            return [""] * len(row)

        st.subheader("📄 Drift Report")

        st.dataframe(report_df.style.apply(highlight_drift, axis=1))

        # -------------------------------
        # DOWNLOAD
        # -------------------------------

        csv = report_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Report",
            csv,
            "drift_report.csv",
            "text/csv"
        )

        st.divider()

        # -------------------------------
        # GRAPH
        # -------------------------------

        st.subheader("📊 Feature Distribution Comparison")

        numeric_cols = reference.select_dtypes(include=["number"]).columns

        selected_feature = st.selectbox("Select Feature", numeric_cols)

        fig = plt.figure()

        plt.hist(reference[selected_feature].dropna(), bins=30, alpha=0.5, label="Reference")
        plt.hist(current[selected_feature].dropna(), bins=30, alpha=0.5, label="Current")

        plt.title(f"{selected_feature} Distribution")
        plt.legend()

        st.pyplot(fig)

else:
    st.warning("🔒 Enter correct admin credentials")