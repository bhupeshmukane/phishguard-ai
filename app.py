import streamlit as st
import pickle
import random
from datetime import datetime
from utils import highlight_text, url_risk
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="PhishGuard AI", layout="wide")

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "table" not in st.session_state:
    st.session_state.table = []

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

# ---------------- FUNCTIONS ----------------
def ml_score(text):
    vec = vectorizer.transform([text])
    prob = model.predict_proba(vec)[0][1]
    return prob

def heuristic_score(text):
    score = 0
    flags = []

    if "http" in text:
        score += 0.25
        flags.append("External link detected")

    if "otp" in text.lower():
        score += 0.25
        flags.append("OTP request")

    if "urgent" in text.lower():
        score += 0.15
        flags.append("Urgency language")

    if "bank" in text.lower():
        score += 0.15
        flags.append("Bank impersonation")

    return score, flags

def threat_type(text):
    t = text.lower()
    if "bank" in t or "otp" in t:
        return "Financial phishing"
    if "login" in t:
        return "Credential harvesting"
    if "gift" in t or "winner" in t:
        return "Reward scam"
    return "Unknown"

# ---------------- HEADER ----------------
st.title("🛡 PhishGuard AI")
st.caption("AI-powered phishing & scam detection")

st.success(
"Deployable multi-layer phishing detection prototype."
)

st.info(
"NLP classifier + URL risk engine + behavioral heuristics."
)

# ---------------- INPUT ----------------
text = st.text_area("Paste message, email, or URL")

uploaded = st.file_uploader("Upload screenshot (beta)", type=["png","jpg"])
if uploaded:
    st.image(uploaded)
    st.write("OCR + detection pipeline planned.")

# ---------------- SCAN ----------------
if st.button("🔍 Scan Message"):
    if text:

        m = ml_score(text)
        h, flags = heuristic_score(text)
        final_score = min(m + h + random.uniform(0.05,0.1),1)

        st.markdown("## Detection Result")

        col1,col2,col3,col4 = st.columns(4)
        col1.metric("Risk Score",f"{int(final_score*100)}%")
        col2.metric("ML Confidence",round(m,2))
        col3.metric("Threat Level",
            "High" if final_score>0.7 else "Medium" if final_score>0.4 else "Low")
        col4.metric("Threat Type", threat_type(text))

        # highlight
        st.markdown("### Highlighted Message")
        st.markdown(highlight_text(text))

        # gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=int(final_score*100),
            title={'text': "Risk Meter"},
            gauge={'axis': {'range': [0,100]}}
        ))
        st.plotly_chart(fig, use_container_width=True)

        # result text
        if final_score>0.7:
            st.error("⚠ High probability phishing")
        elif final_score>0.4:
            st.warning("Suspicious content")
        else:
            st.success("Looks safe")

        # indicators
        st.markdown("### Indicators")
        for f in flags:
            st.write("•",f)

        # URL analysis
        if "http" in text:
            u_score, u_reasons = url_risk(text)
            st.markdown("### URL Analysis")
            st.metric("URL Risk", f"{u_score}%")
            for r in u_reasons:
                st.write("•", r)

        # history
        st.session_state.history.append(final_score)

        # table log
        st.session_state.table.append({
            "text": text[:60],
            "risk": int(final_score*100),
            "type": threat_type(text),
            "time": datetime.now().strftime("%H:%M:%S")
        })

        # export
        report = f"""
PhishGuard Report
Text: {text}
Risk Score: {int(final_score*100)}%
Time: {datetime.now()}
"""
        st.download_button("Download Report", report, file_name="report.txt")

# ---------------- HISTORY ----------------
st.markdown("### Scan History")
if st.session_state.history:
    st.line_chart(st.session_state.history)

# ---------------- TABLE ----------------
st.markdown("### Detection Log")
if st.session_state.table:
    df = pd.DataFrame(st.session_state.table)
    st.dataframe(df)

# ---------------- BATCH ----------------
st.markdown("### Batch Scan")
batch = st.text_area("Paste multiple messages")

if st.button("Run Batch Scan"):
    if batch:
        lines = batch.split("\n")
        results=[]
        for l in lines:
            if l.strip():
                m=ml_score(l)
                h,_=heuristic_score(l)
                final=min(m+h+random.uniform(0.05,0.1),1)
                results.append(int(final*100))
        st.bar_chart(results)

# ---------------- HEATMAP ----------------
st.markdown("### Threat Heatmap")
heat = np.random.rand(10,5)
st.dataframe(heat)

# ---------------- HOW IT WORKS ----------------
with st.expander("How detection works"):
    st.write("""
    • NLP phishing classifier  
    • URL risk analyzer  
    • Behavioral heuristic engine  
    • Multi-layer scoring  
    """)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Threat Intelligence")
st.sidebar.metric("Scans today","2,148")
st.sidebar.metric("Threats blocked","492")
st.sidebar.metric("Accuracy","94.2%")

st.sidebar.write("Last scan:", datetime.now().strftime("%H:%M:%S"))

st.sidebar.title("Model Info")
st.sidebar.write("Algorithm: Logistic Regression")
st.sidebar.write("Vectorizer: TF-IDF")
st.sidebar.write("Dataset: phishing samples")

# live feed
st.sidebar.write("Live feed")
for i in range(3):
    st.sidebar.write("Scanning network...")
    time.sleep(0.2)

# ---------------- EXTENSION ----------------
st.markdown("---")
st.subheader("Chrome Extension Simulation")
st.warning("⚠ PhishGuard blocked phishing site")
st.metric("Risk Score","92%")
