import streamlit as st

st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💰"
)

st.title("💰 Finance Dashboard")

st.write("My personal financial overview")

st.metric(
    label="Total Net Worth",
    value="£0.00"
)