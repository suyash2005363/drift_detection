import streamlit as st

st.set_page_config(page_title="Drift Detection System")

st.title("📊 Drift Detection Project")

st.write("Welcome! Choose an option:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Admin Login"):
        st.switch_page("pages/Admin.py")

with col2:
    if st.button("➡️ Continue (Prediction)"):
        st.switch_page("pages/Continue.py")