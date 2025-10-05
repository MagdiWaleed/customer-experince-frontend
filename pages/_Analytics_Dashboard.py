# dashboard_app.py
import streamlit as st
import requests

st.set_page_config(page_title="Admin Dashboard Analytics", layout="wide")
st.title("📊 Admin Dashboard Analytics")

API_STATS_URL = "https://8000-dep-01k6sj99nxkqpr1m5srkmwgyk8-d.cloudspaces.litng.ai/dashboard/"  

try:
    resp = requests.get(API_STATS_URL)
    stats = resp.json()
except Exception as e:
    st.warning(f"Could not fetch dashboard stats: {e}")
    stats = {
        "total_procedures": 0,
        "total_steps": 0,
        "total_complaints": 0,
        "total_tickets": 0,
        "total_amount_complaints": 0.0,
        "most_complaint_product": None,
        "most_complaint_subscription": None
    }

st.subheader("📈 Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Procedures", stats.get("total_procedures", 0))
col2.metric("Total Steps", stats.get("total_steps", 0))
col3.metric("Total Tickets", stats.get("total_tickets", 0))

col4, col5, col6 = st.columns(3)
col4.metric("Total Complaints", stats.get("total_complaints", 0))
col6.metric("Total Amount of Complaints ($)", stats.get("total_amount_complaints", 0.0))