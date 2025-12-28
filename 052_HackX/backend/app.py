import streamlit as st
import json
import os
import matplotlib.pyplot as plt

from process_session import process_session
from llm_analysis import render_snapshot, analyze_with_llm

st.set_page_config(page_title="Focus Drift", layout="centered")

st.title("🧠 Focus Drift")
st.caption("A quiet look at how your attention moved during a work session.")

# ---- Load session data ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "latest_session.json")

if not os.path.exists(SESSION_PATH):
    st.error("No session data found.")
    st.stop()

with open(SESSION_PATH, "r") as f:
    session = json.load(f)

metrics = process_session(session)

# ---- Snapshot ----
st.subheader("Session Snapshot")
st.text(render_snapshot(metrics))

# ---- Graph 1: Time spent per domain ----
st.subheader("Where your time went")

domains = [d["domain"] for d in metrics.get("topDomains", [])]
times = [d["estimatedTimeSec"] for d in metrics.get("topDomains", [])]

if domains:
    fig, ax = plt.subplots()
    ax.bar(domains, times)
    ax.set_ylabel("Seconds")
    ax.set_xlabel("Website")
    ax.set_title("Estimated time spent per site")

    st.pyplot(fig)
else:
    st.write("Not enough data to show domain breakdown.")

# ---- Graph 2: Switching intensity ----
st.subheader("How jumpy the session was")

st.metric(
    label="Tab switches per minute",
    value=round(metrics["switchRatePerMin"], 1)
)

# ---- LLM Insight ----
st.subheader("Focus Drift Insight")

with st.spinner("Analyzing session..."):
    insight = analyze_with_llm(metrics)

st.markdown(insight)