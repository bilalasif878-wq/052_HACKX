import streamlit as st
import os
import json
from process_session import process_session
from llm_analysis import analyze_with_llm

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Focus Drift",
    page_icon="🧠",
    layout="centered"
)

# ------------------------------
# STYLING
# ------------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.card {
    background: #020617;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 18px;
}

.title {
    font-size: 26px;
    font-weight: 700;
}

.subtitle {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 12px;
}

.metric {
    color: #94a3b8;
    font-size: 13px;
}

.value {
    font-size: 22px;
    font-weight: bold;
    color: #f8fafc;
}

.bar-bg {
    background: #1e293b;
    border-radius: 6px;
    height: 8px;
    margin-top: 6px;
}

.bar-fill {
    background: #6366f1;
    height: 100%;
    border-radius: 6px;
}

.section-title {
    font-size: 18px;
    margin-top: 10px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# LOAD SESSION
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "latest_session.json")

if not os.path.exists(SESSION_PATH):
    st.warning("No session recorded yet.")
    st.stop()

with open(SESSION_PATH) as f:
    session = json.load(f)

metrics = process_session(session)

# ------------------------------
# HEADER
# ------------------------------
st.markdown("<div class='title'>Focus Drift</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A quiet look at how your attention moved.</div>", unsafe_allow_html=True)

# ------------------------------
# SESSION DURATION (FIXED)
# ------------------------------
total_seconds = metrics["durationSec"]
minutes = total_seconds // 60
seconds = total_seconds % 60

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='metric'>Session Duration</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='value'>{minutes} min {seconds} sec</div>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# FOCUS SCORE
# ------------------------------
focus_score = max(0, 100 - int(metrics["switchRatePerMin"] * 6))

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='metric'>Focus Score</div>", unsafe_allow_html=True)
st.markdown(f"<div class='value'>{focus_score} / 100</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="bar-bg">
    <div class="bar-fill" style="width:{focus_score}%"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# USAGE BREAKDOWN
# ------------------------------
st.markdown("<div class='section-title'>Usage Breakdown</div>", unsafe_allow_html=True)

max_time = max([d["estimatedTimeSec"] for d in metrics["topDomains"]] or [1])

for d in metrics["topDomains"]:
    pct = int((d["estimatedTimeSec"] / max_time) * 100)

    st.markdown(f"""
    <div class="card">
        <div class="metric">{d['domain']}</div>
        <div class="bar-bg">
            <div class="bar-fill" style="width:{pct}%"></div>
        </div>
        <div class="metric">{d['estimatedTimeSec']} sec</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# AI INSIGHT
# ------------------------------
st.markdown("<div class='section-title'>Focus Insight</div>", unsafe_allow_html=True)

with st.spinner("Analyzing your session..."):
    insight = analyze_with_llm(metrics)

st.markdown(f"""
<div class="card">
{insight}
</div>
""", unsafe_allow_html=True)

