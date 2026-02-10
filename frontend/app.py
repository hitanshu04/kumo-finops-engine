import streamlit as st
import requests
import pandas as pd
import os

# 1. GET THE URL FROM DOCKER ENV (Defaults to localhost if not found)
API_URL = "https://kumo-finops-engine.onrender.com"

st.set_page_config(page_title="Kumo FinOps", page_icon="☁️", layout="wide")
st.title("☁️ Kumo: Cloud Cost Intelligence")

# 2. Sidebar: Add New Data
st.sidebar.header("💸 Add New Expense")
service = st.sidebar.selectbox(
    "Service Provider", ["AWS EC2", "AWS RDS", "Google Cloud Storage", "Azure VM"])
amount = st.sidebar.number_input("Cost ($)", min_value=0.0, format="%.2f")

if st.sidebar.button("Submit Expense"):
    payload = {"service": service, "amount": amount}
    try:
        response = requests.post(f"{API_URL}/ingest/", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.sidebar.success(f"Saved! ID: {data['id']}")
            if data['is_anomaly']:
                st.sidebar.error("🚨 ANOMALY DETECTED! (Alert sent to Slack)")
        else:
            st.sidebar.error("Failed to save data")
    except Exception as e:
        st.sidebar.error(f"Connection Error: {e}")

# 3. Main Dashboard
st.subheader("📊 Live Spending Feed")

try:
    response = requests.get(f"{API_URL}/costs/")
    if response.status_code == 200:
        costs = response.json()
        if costs:
            df = pd.DataFrame(costs)

            # Show Metrics
            total_spend = df['amount'].sum()
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Spend", f"${total_spend:,.2f}")
            col2.metric("Total Transactions", len(df))
            col3.metric("Anomalies Detected", len(
                df[df['is_anomaly'] == True]))

            # Show Data & Graph
            st.dataframe(df.sort_values(by="timestamp",
                         ascending=False), use_container_width=True)
            st.subheader("📈 Cost Trend")
            st.line_chart(df.set_index("timestamp")["amount"])
        else:
            st.info("No data found. Add some expenses!")
    else:
        st.error("Backend returned an error.")
except Exception as e:
    st.error(f"Could not connect to Backend at {API_URL}. Is Docker running?")
