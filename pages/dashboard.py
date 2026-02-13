import streamlit as st
import random

st.title("📊 Threat Dashboard")

scans = random.randint(1500,3000)
phish = random.randint(300,700)

st.metric("Messages scanned", scans)
st.metric("Phishing detected", phish)
st.metric("Detection rate", f"{round(phish/scans*100,1)}%")

st.subheader("Threat trend")
st.line_chart([5,8,3,10,7,12,9])

st.subheader("Top attack types")
st.bar_chart([20,35,15,40])
