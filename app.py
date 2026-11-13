import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Flower Lab | Federated Learning", page_icon="✿", layout="wide")

st.markdown("""
<style>
.stApp {background: radial-gradient(circle at 70% -10%, #1b2b50 0, transparent 38%), #080d1b; color:#edf3ff}
section[data-testid="stSidebar"] {background:#0b1223}
.block-container {padding-top:1.6rem; max-width:1500px}
h1,h2,h3,p,label {color:#edf3ff}
div[data-testid="stMetric"] {background:#111a30;border:1px solid #273653;padding:14px;border-radius:12px}
div[data-testid="stMetric"] label {color:#91a0bd}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {color:#edf3ff}
.panel {background:linear-gradient(145deg,#121c33,#0f172a);border:1px solid #273653;border-radius:13px;padding:17px;margin-bottom:14px}
.muted {color:#91a0bd;font-size:12px}
.node {background:#151f39;border:1px solid #314363;border-radius:10px;padding:15px;text-align:center}
.server {background:#201d49;border:1px solid #6855d2;border-radius:12px;padding:16px;text-align:center;max-width:420px;margin:0 auto 14px}
.tag {display:inline-block;background:#12372f;color:#62e4b7;border:1px solid #1d5b4b;padding:4px 9px;border-radius:18px;font-size:11px}
div.stButton > button {border-radius:8px}
</style>
""", unsafe_allow_html=True)

if "stage" not in st.session_state:
    st.session_state.stage = 5
if "running" not in st.session_state:
    st.session_state.running = False
if "logs" not in st.session_state:
    st.session_state.logs = [
        "[15:04:01] INFO Flower SuperGrid run initialized",
        "[15:04:03] SERVER Global model initialized · FedAvg",
        "[15:04:05] CLIENT Client 1, Client 2, Client 3 connected",
        "[15:04:12] TRAIN Local training completed on all clients",
        "[15:04:15] AGGREGATE Received 3 results and 0 failures",
        "[15:04:17] DONE Run completed · 1 round",
    ]

def add_log(msg):
    st.session_state.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

st.sidebar.markdown("## ✿ Flower Lab")
st.sidebar.caption("APRILLIA WORKSPACE")
page = st.sidebar.radio("WORKSPACE", ["Dashboard", "Simulation", "Clients", "Training Metrics", "Run Logs"])
st.sidebar.divider()
st.sidebar.caption("Project: flwrlabs/fed-legal-llm")
st.sidebar.caption("Federated Learning Demo")

st.title("Federated Learning Dashboard")
st.caption("Flower Lab  ›  Project Dashboard")
st.warning("DEMO VIEW — Dashboard interaktif untuk memperlihatkan alur 1 server dan 3 client. Ini bukan koneksi langsung ke Flower SuperGrid.")
c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
with c1:
    if st.button("▶ Start Simulation", use_container_width=True, type="primary"):
        st.session_state.stage = 0
        st.session_state.running = True
        add_log("INFO Simulation started")
with c2:
    if st.button("Ⅱ Pause", use_container_width=True):
        st.session_state.running = False
        add_log("INFO Simulation paused")
with c3:
    if st.button("↻ Reset", use_container_width=True):
        st.session_state.stage = 0
        st.session_state.running = False
        add_log("INFO Simulation reset")
with c4:
    if st.button("Next Step", use_container_width=True):
        st.session_state.stage = min(5, st.session_state.stage + 1)
        add_log(f"SIMULATION Stage advanced to {st.session_state.stage}/5")

stage = st.session_state.stage
st.markdown(f'<span class="tag">{"RUNNING" if st.session_state.running else ("COMPLETED" if stage == 5 else "READY / PAUSED")}</span> &nbsp; <span class="muted">Round 1 / 1 · Stage {stage}/5</span>', unsafe_allow_html=True)
st.write("")

if page in ["Dashboard", "Simulation", "Clients"]:
    left, right = st.columns([1.55, 0.85], gap="large")
    with left:
        st.markdown('<div class="panel"><b>PROJECT DASHBOARD — ALL NODES</b><div class="muted">Server coordination and client topology</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="server"><b>🟣 Flower Server</b><br><span class="muted">Global Model · FedAvg Aggregator</span></div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, col in enumerate(cols, start=1):
            pct = 100 if stage >= 5 else (75 if stage >= 3 else (35 if stage >= 2 else 0))
            state = "Completed" if stage >= 5 else ("Training / Update" if stage >= 2 else "Waiting")
            with col:
                st.markdown(f'<div class="node"><b>▣ Client {i}</b><br><span class="muted">SuperNode · Local Dataset {i}</span><br><br><span class="tag">{state}</span></div>', unsafe_allow_html=True)
                st.progress(pct)
    with right:
        st.markdown('<div class="panel"><b>PROJECT WORKFLOW / ACTIVITY PROGRESS</b><div class="muted">Federated training stages</div></div>', unsafe_allow_html=True)
        steps = ["Initialize global model", "Distribute global model", "Local training", "Aggregate client updates", "Update global model"]
        for i, step in enumerate(steps, start=1):
            state = "DONE" if stage >= i else ("NEXT" if stage == i-1 else "WAITING")
            st.write(("✅" if stage >= i else "◯") + "  " + step)
            st.caption(state)
            st.progress(1.0 if stage >= i else 0.0)

if page in ["Dashboard", "Training Metrics"]:
    st.subheader("Training Loss — Log Flower")
    # Synthetic illustrative curve, not raw metrics from the actual Flower run.
    rng = np.random.default_rng(11)
    x = np.arange(1, 79)
    y = 3.72 - 0.0045*x + rng.normal(0, 0.075, size=78)
    y = np.clip(y, 3.25, 3.95)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Global training loss",
                             line=dict(color="#43d7e8", width=2)))
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(8,15,32,0.55)", height=300,
                      margin=dict(l=10,r=10,t=10,b=10),
                      xaxis_title="Training step", yaxis_title="Loss")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Kurva di atas adalah data ilustratif untuk demo dashboard. Laporan run Flower mencatat 78 titik loss gabungan, tetapi data mentah tiap titik tidak tersedia.")

if page in ["Dashboard", "Run Logs"]:
    st.subheader("Flower CLI — Live Output")
    st.code("\n".join(st.session_state.logs[-14:]), language="text")

if page in ["Dashboard", "Clients", "Simulation"]:
    st.subheader("Run Summary")
    a,b,c,d = st.columns(4)
    a.metric("Server Round", "1 / 1")
    b.metric("Clients Completed", f"{3 if stage >= 5 else 0 if stage < 2 else 3} / 3")
    c.metric("Updates Received", "3" if stage >= 4 else "—")
    d.metric("Training Failures", "0" if stage >= 4 else "—")

st.divider()
st.caption("Historical Flower SuperGrid run ID: 14714596137151743331 · Status Completed (sesuai laporan). Run nyata dan dashboard demo ini adalah dua hal berbeda.")
