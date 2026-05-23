import streamlit as st
import time
import random

# App Configuration
st.set_page_config(page_title="AI Focus Drift Detector", page_icon="🧠", layout="wide")

st.title("🧠 AI Focus Drift Detector")
st.caption("A behavioural AI prototype for tracking student concentration metrics.")

# Initialize Session States for Data Tracking
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'rt_clicks' not in st.session_state:
    st.session_state.rt_clicks = []
if 'distractions' not in st.session_state:
    st.session_state.distractions = 0

# Sidebar - Live Metrics Dashboard
st.sidebar.header("📊 Real-Time Telemetry")
elapsed_time = round(time.time() - st.session_state.start_time, 1)
st.sidebar.metric(label="Study Session Duration", value=f"{elapsed_time} seconds")

# 1. Behavioural Tracking: Distraction Logger
st.subheader("🤖 Behavioural Tracking")
col1, col2 = st.columns(2)

with col1:
    st.write("Log whenever you look away, check your phone, or switch tabs:")
    if st.button("⚠️ Log Focus Drift/Distraction Event"):
        st.session_state.distractions += 1

with col2:
    st.metric(label="Logged Distraction Events", value=st.session_state.distractions, delta="- Lower is Better")

# 2. Cognitive Performance: Reaction Time Mini-Test
st.subheader("⚡ Cognitive Performance Test")
st.write("Click the button as fast as you can when it appears to test your processing speed.")

# Simple Reaction Test Simulator
if st.button("🎯 Trigger Reaction Test"):
    wait_time = random.uniform(0.5, 2.0)
    time.sleep(wait_time)
    
    test_start = time.time()
    if st.button("CLICK NOW!"):
        rt = round((time.time() - test_start) * 1000, 2)
        st.session_state.rt_clicks.append(rt)
        st.success(f"Reaction Time: {rt} ms")

# Show historical reaction data
if st.session_state.rt_clicks:
    st.line_chart(st.session_state.rt_clicks)
    avg_rt = round(sum(st.session_state.rt_clicks) / len(st.session_state.rt_clicks), 2)
    st.metric(label="Average Reaction Time", value=f"{avg_rt} ms")
else:
    st.info("No reaction data collected yet. Click the trigger button above.")

# 3. AI Predictive Core (Algorithmic Heuristic)
st.subheader("🔮 Predictive Analytics")

# Calculate a basic focus score
base_score = 100
deductions = (st.session_state.distractions * 15)

if st.session_state.rt_clicks:
    current_avg = sum(st.session_state.rt_clicks) / len(st.session_state.rt_clicks)
    # Penalize score if reaction times slow down past 400ms
    if current_avg > 400:
        deductions += int((current_avg - 400) / 10)

focus_score = max(0, min(100, base_score - deductions))

# Focus Display Indicators
if focus_score > 75:
    st.success(f"🔥 Focus Score: {focus_score}% — Optimal learning state detected.")
elif focus_score > 40:
    st.warning(f"⚠️ Focus Score: {focus_score}% — Focus drift detected. Consider changing your task.")
else:
    st.error(f"🛑 Focus Score: {focus_score}% — Severe concentration drop. Time for a 5-minute break!")
  
