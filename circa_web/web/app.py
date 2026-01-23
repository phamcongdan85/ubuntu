import streamlit as st
from circa_runner import run_circa

st.set_page_config(layout="wide")
st.title("CIRCA – Root Cause Analysis")

if st.button("Run CIRCA"):
    with st.spinner("Running RCA..."):
        result = run_circa()

    st.subheader("Root Cause Ranking")
    st.table(result)
