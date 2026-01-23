import streamlit as st
import requests

st.set_page_config(page_title="Credit Risk Scoring", layout="centered")

st.title("🏦 Credit Risk Scoring")

customer_id = st.number_input(
    "Customer ID",
    min_value=1,
    step=1
)

if st.button("Score"):
    with st.spinner("Scoring..."):
        res = requests.get(
            f"http://backend:8000/predict/{int(customer_id)}"
        )

    if res.status_code == 200:
        pd_value = res.json()["probability_of_default"]
        st.success(f"Probability of Default (PD): {pd_value}")
    elif res.status_code == 404:
        st.error("Customer ID not found")
    else:
        st.error("Scoring failed")
