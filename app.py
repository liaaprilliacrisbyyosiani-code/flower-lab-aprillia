import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(page_title="Flower Lab | Federated Learning", page_icon="✿", layout="wide")

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 70% -10%,#1b2b50 0,transparent 38%),#080d1b;color:#edf3ff}
section[data-testid="stSidebar"]{background:#0b1223}
.block-container{padding-top:1.5rem;max-width:1500px}
h1,h2,h3,p,label{color:#edf3ff}
div[data-testid="stMetric"]{background:#111a30;border:1px solid #273653;padding:13px;border-radius:12px}
div[data-testid="stMetric"] label{color:#91a0bd}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#edf3ff}
.panel{background:linear-gradient(145deg,#121c33,#0f172a);border:1px solid #273653;border-radius:13px;padding:16px;margin-bottom:12px}
.server{background:#201d49;border:1px solid #6855d2;border-radius:12px;padding:15px;text-align:center;margin:8px auto 14px;max-width:440px}
.node{background:#151f39;border:1px solid #314363;border-radius:10px;padding:12px;text-align:center}
.tag{display:inline-block;background:#12372f;color:#62e4b7;border:1px solid #1d5b4b;padding:4px 9px;border-radius:18px;font-size:11px}
.smallmuted{color:#91a0bd;font-size:12px}
div.stButton>button{border-radius:8px}
</style>
""", unsafe_allow_html=True)

STEPS = [
    ("Initialize global model", "Server menyiapkan model global dan adapter awal."),
    ("Distribute global model", "Server mengirim model global ke Client 1, Client 2, dan Client 3."),
    ("Local training", "Ketiga client menjalankan training lokal pada dataset masing-masing."),
    ("Aggregate client updates", "Server menerima 3 update dan menjalankan agregasi FedAvg."),
    ("Update global model", "Model global diperbarui dan round dinyatakan selesai."),
]

if "stage" not in st.session_state:
    st.session_state.stage = 5
if "logs" not in st.session_state:
    st.session_state.logs = [
        "[Riwayat demo] Flower Server initialized · FedAvg",
        "[Riwayat demo] Client 1, Client 2, Client 3 connected",
        "[Riwayat demo] Received 3 results and 0 failures",
        "[Riwayat demo] Run completed · 1 round",
    ]
if "status" not in st.session_state:
    st.session_state.status = "COMPLETED"

def addlog(message):
    st.session_state.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

st.sidebar.markdown("## ✿ Flower Lab")
st.sidebar.caption("APRILLIA WORKSPACE")
page = st.sidebar.radio("WORKSPACE", ["Dashboard", "Simulation", "Clients", "Training Metrics", "Run Logs"])
st.sidebar.divider()
st.sidebar.caption("Project: flwrlabs/fed-legal-llm")
st.sidebar.caption("Federated Learning Demo")

st.title("Federated Learning Dashboard")
st.caption("Flower Lab  ›  Project Dashboard")
st.warning("DEMO VIEW — Simulasi visual interaktif 1 server dan 3 client. Halaman ini tidak terhubung langsung ke Flower SuperGrid.")

c1,c2,c3 = st.columns([1.25,1,1])
with c1:
    start = st.button("▶ Start Simulation", type="primary", use_container_width=True)
with c2:
    pause = st.button("Ⅱ Pause", use_container_width=True)
with c3:
    reset = st.button("↻ Reset", use_container_width=True)

if reset:
    st.session_state.stage = 0
    st.session_state.status = "READY"
    st.session_state.logs = []
    addlog("INFO Simulation reset. Ready to start.")
if pause:
    st.session_state.status = "PAUSED"
    addlog("INFO Pause selected. Use Start Simulation to run the demo again.")
if start:
    st.session_state.stage = 0
    st.session_state.status = "RUNNING"
    st.session_state.logs = []
    addlog("INFO Simulation started")
    status_slot = st.empty()
    progress_slot = st.empty()
    detail_slot = st.empty()
    for idx, (name, description) in enumerate(STEPS, start=1):
        st.session_state.stage = idx
        addlog(f"STEP {idx}/5 · {name}")
        if idx == 1:
            addlog("SERVER Global model initialized")
        elif idx == 2:
            addlog("SERVER Global model distributed to 3 clients")
        elif idx == 3:
            addlog("CLIENT Client 1, Client 2, Client 3 local training completed")
        elif idx == 4:
            addlog("AGGREGATE Received 3 results and 0 failures · FedAvg")
        elif idx == 5:
            addlog("SERVER Global model updated · Round 1 completed")
        status_slot.markdown(f'<span class="tag">RUNNING · STEP {idx}/5</span> &nbsp; {name}', unsafe_allow_html=True)
        progress_slot.progress(idx/5, text=f"Progress simulasi: {idx*20}%")
        detail_slot.info(description)
        time.sleep(0.85)
    st.session_state.status = "COMPLETED"
    addlog("DONE Simulation completed successfully · 1 server · 3 clients · 1 round")
    st.success("Simulasi selesai! Ketiga client telah mengirimkan update dan server menyelesaikan agregasi FedAvg.")
    st.rerun()

stage = st.session_state.stage
status = st.session_state.status
st.markdown(f'<span class="tag">{status}</span> &nbsp; <span class="smallmuted">Round 1 / 1 · Stage {stage}/5</span>', unsafe_allow_html=True)

if page in ["Dashboard","Simulation","Clients"]:
    left,right = st.columns([1.55,.85],gap="large")
    with left:
        st.markdown('<div class="panel"><b>PROJECT DASHBOARD — ALL NODES</b><br><span class="smallmuted">Server coordination and client topology</span></div>',unsafe_allow_html=True)
        st.markdown('<div class="server"><b>🟣 Flower Server</b><br><span class="smallmuted">Global Model · FedAvg Aggregator</span></div>',unsafe_allow_html=True)
        cols = st.columns(3)
        for i,col in enumerate(cols,1):
            if stage >= 5:
                state,pct="COMPLETED",100
            elif stage >= 3:
                state,pct="TRAINING / UPDATE",75
            elif stage >= 2:
                state,pct="MODEL RECEIVED",35
            else:
                state,pct="WAITING",0
            with col:
                st.markdown(f'<div class="node"><b>▣ Client {i}</b><br><span class="smallmuted">SuperNode · Local Dataset {i}</span><br><br><span class="tag">{state}</span></div>',unsafe_allow_html=True)
                st.progress(pct/100)
    with right:
        st.markdown('<div class="panel"><b>PROJECT WORKFLOW / ACTIVITY PROGRESS</b><br><span class="smallmuted">Federated training stages</span></div>',unsafe_allow_html=True)
        for i,(name,desc) in enumerate(STEPS,1):
            if stage >= i:
                st.write("✅  "+name)
                st.caption("DONE")
                st.progress(1.0)
            elif stage == i-1 and status == "RUNNING":
                st.write("🔄  "+name)
                st.caption("RUNNING")
                st.progress(0.5)
            else:
                st.write("◯  "+name)
                st.caption("WAITING")
                st.progress(0.0)

if page in ["Dashboard","Training Metrics"]:
    st.subheader("Training Loss — Log Flower")
    # Illustrative curve only; raw 78 loss values from the historical run are not available.
    rng=np.random.default_rng(11)
    x=np.arange(1,79)
    y=3.72-0.0045*x+rng.normal(0,0.075,size=78)
    y=np.clip(y,3.25,3.95)
    fig=go.Figure(go.Scatter(x=x,y=y,mode="lines",name="Illustrative training loss",line=dict(color="#43d7e8",width=2)))
    fig.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(8,15,32,0.55)",height=290,margin=dict(l=8,r=8,t=10,b=10),xaxis_title="Training step",yaxis_title="Loss")
    st.plotly_chart(fig,use_container_width=True)
    st.caption("Grafik ini menggunakan data ilustratif untuk demo. Laporan run historis mencatat 78 titik loss gabungan, tetapi nilai mentah setiap titik tidak tersedia.")

if page in ["Dashboard","Run Logs"]:
    st.subheader("Flower CLI — Activity Log")
    st.code("\n".join(st.session_state.logs[-20:]) or "Belum ada aktivitas. Klik Start Simulation.",language="text")

if page in ["Dashboard","Clients","Simulation"]:
    st.subheader("Run Summary")
    a,b,c,d=st.columns(4)
    a.metric("Server Round","1 / 1" if stage>=5 else "0 / 1")
    b.metric("Clients Completed",f"{3 if stage>=5 else 0} / 3")
    c.metric("Updates Received","3" if stage>=4 else "0")
    d.metric("Training Failures","0")

st.divider()
st.caption("Historical Flower SuperGrid run ID: 14714596137151743331 · Completed (sesuai laporan). Simulasi visual ini terpisah dari run Flower nyata.")
