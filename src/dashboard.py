# -*- coding: utf-8 -*-
"""
Macroeconomic Regime Tracker Presentation Layer
Enterprise Hotfix Build v2 | Target: Absolute Key-State Binding
Created: 2026-07-28 | Author: hsc
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analytics_engine import run_vocabulary_analysis, get_countdown_metrics

# --- 1. DEFENSIVE PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Macroeconomic Regime Tracker",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- 2. INJECT CSS STYLING SPECIFICATIONS ---
st.markdown("""
<style>
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
[data-testid="stSidebarUserContent"] { padding-top: 1.5rem !important; }
.stMarkdown h3, .stMarkdown p { margin-bottom: 0px !important; padding-bottom: 4px !important; }
hr { margin-top: 10px !important; margin-bottom: 14px !important; }
[data-testid="stVerticalBlock"] { gap: 0.4rem !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. HIGH-PRECISION ENGINEERING CALLBACK LAYER ---
def trigger_param_reset():
    st.session_state["max_df_val"] = 0.85
    st.session_state["min_len_val"] = 3
    st.session_state["anomaly_th_val"] = 52.10

# --- 4. SIDEBAR PARAMETER INTERFACE ---
st.sidebar.header("⚙️ Model Controls")
st.sidebar.markdown("Adjust interactive weights for the underlying NLP core math pipeline.")

# Initialize stable session state parameters if they don't exist yet
if "max_df_val" not in st.session_state:
    st.session_state["max_df_val"] = 0.85
if "min_len_val" not in st.session_state:
    st.session_state["min_len_val"] = 3
if "anomaly_th_val" not in st.session_state:
    st.session_state["anomaly_th_val"] = 52.10

# ENTERPRISE PATCH V2: Leverage explicit keys instead of value parameters to lock two-way UI binding
max_df_slider = st.sidebar.slider(
    "Max Document Frequency (max_df)", 
    min_value=0.50, 
    max_value=1.00, 
    key="max_df_val", 
    step=0.05
)
min_word_len = st.sidebar.slider(
    "Minimum Word Character Length", 
    min_value=2, 
    max_value=6, 
    key="min_len_val", 
    step=1
)
anomaly_threshold = st.sidebar.slider(
    "Regime Shift Anomaly Threshold (%)", 
    min_value=10.0, 
    max_value=90.0, 
    key="anomaly_th_val", 
    step=0.10
)

# Trigger state adjustments cleanly via Streamlit's official callback parameter
st.sidebar.button("🔄 Reset Parameters to Default", on_click=trigger_param_reset, use_container_width=True)
st.sidebar.divider()

# --- LIVE COUNTDOWN BLOCK ELEMENT ---
release_date_str, days_remaining = get_countdown_metrics()
st.sidebar.markdown(
    f"""
    <div style="background-color: #f0f2f6; padding: 12px; border-radius: 8px; border-left: 5px solid #1f77b4; margin-bottom: 5px;">
        <span style="font-size: 12px; color: #555555; text-transform: uppercase; font-weight: bold;">Next Minutes Release</span>
        <h2 style="margin: 0; padding: 2px 0; color: #1f77b4; font-size: 26px; font-weight: 800;">{release_date_str}</h2>
        <span style="font-size: 14px; color: #333333; font-weight: 600;">⏳ {days_remaining} Days Remaining</span>
    </div>
    """, unsafe_allow_html=True
)
st.sidebar.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# SYSTEM CONTEXT NOTES
st.sidebar.markdown(
    "**System Context:**\n"
    "• IDE Workspace: Terminal Core\n"
    "• Server Runtime: Streamlit Local Laboratory\n"
    "• Database Ledger: `fomc_cleaned_data.json`"
)

# --- 5. MAIN DASHBOARD CONTENT HEADERS ---
st.title("📑 Unsupervised Language Analytics Engine")
st.subheader("Macroeconomic Policy Shifts & Policy Regime Discontinuity Tracker")
st.markdown(
    "This engine tracks structural text adjustments between sequential FOMC minutes using "
    "**TF-IDF Feature Vectorization** and **Cosine Distance Vector Space Analysis**. "
    "Spikes represent structural vocabulary adjustments across sequential policy meetings."
)
st.divider()

# --- 6. ENGINE MATH PAYLOAD EXECUTION ---
with st.spinner("Executing background mathematical NLP pipeline..."):
    payload = run_vocabulary_analysis(max_df_param=max_df_slider, word_length=min_word_len, threshold_param=anomaly_threshold)

if payload is None:
    st.error("❌ Data Ledger Failure: Unable to locate or parse `fomc_cleaned_data.json` in the active workspace directory.")
    st.stop()

# --- 7. REAL-TIME SYSTEM STATUS & ANALYST FOCUS NODE ---
st.markdown(f"## 🔍 Focus Node: {payload['latest_date']}")
variance_vs_mean = payload['latest_shift'] - payload['historical_mean']
sign = "+" if variance_vs_mean > 0 else ""

with st.container():
    col1, col2, col3, col4 = st.columns([1.0, 1.0, 1.3, 2.1], gap="medium", vertical_alignment="center")
    with col1:
        st.markdown("<span style='font-size: 14px; color: #555555; font-weight: 500;'>Latest Shift</span>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='margin:0; padding:0; color:#1f77b4; font-size:48px; font-weight:800; line-height:1;'>{payload['latest_shift']:.2f}%</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown("<span style='font-size: 14px; color: #555555; font-weight: 500;'>Baseline Mean</span>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='margin:0; padding:0; color:#333333; font-size:48px; font-weight:700; line-height:1;'>{payload['historical_mean']:.2f}%</h1>", unsafe_allow_html=True)
    with col3:
        if payload['latest_shift'] > anomaly_threshold:
            st.error(f"🚨 **ANOMALY DETECTED**\n\nThreshold Breached.\n\n**{sign}{variance_vs_mean:.2f}% vs Mean**")
        else:
            st.success(f"✅ **REGIME STABLE**\n\nBelow Threshold Limit.\n\n**{sign}{variance_vs_mean:.2f}% vs Mean**")
    with col4:
        st.markdown("**Top Token Variances:**")
        sub_col1, sub_col2 = st.columns(2, gap="medium")
        with sub_col1:
            for word in payload['latest_keywords'][:2]:
                st.markdown(f"<div style='font-size:22px; font-weight:600; color:#2e7d32; white-space:nowrap; line-height:1.4;'>• {word}</div>", unsafe_allow_html=True)
        with sub_col2:
            for word in payload['latest_keywords'][2:4]:
                st.markdown(f"<div style='font-size:22px; font-weight:600; color:#2e7d32; white-space:nowrap; line-height:1.4;'>• {word}</div>", unsafe_allow_html=True)

st.divider()

# --- 8. STRUCTURAL FIXED BASELINE CHART RENDERING ---
fig, ax = plt.subplots(figsize=(14, 4.2))
ax.plot(payload['dates'], payload['shifts'], marker='o', color='#1f77b4', linewidth=2, linestyle='-', label='Vocabulary Shift %')
ax.axhline(payload['historical_mean'], color='red', linestyle='--', alpha=0.7, label=f'Historical Baseline Mean ({payload["historical_mean"]:.2f}%)')
ax.set_title('FOMC Policy Vocabulary Displacement Over Time', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Meeting Date', fontsize=11, labelpad=10)
ax.set_ylabel('True Vocabulary Profile Shift (%)', fontsize=12, labelpad=10)

visible_ticks = range(0, len(payload['dates']), 4)
ax.set_xticks(visible_ticks)
ax.set_xticklabels([payload['dates'][i] for i in visible_ticks], rotation=45, ha='right', fontsize=9)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right')
plt.tight_layout()
st.pyplot(fig)

st.divider()

# --- 9. DETAILED GRANULAR AUDIT LEDGER & DYNAMIC INSPECTOR ---
left_panel, right_panel = st.columns([1.4, 1], gap="medium")
with left_panel:
    st.subheader("📋 Inter-Meeting Policy Drift Index")
    true_historical_keywords = payload.get('top_words_history', [payload['latest_keywords']] * len(payload['dates']))
    historical_matrix = pd.DataFrame({
        "Policy Meeting Date": payload['dates'],
        "Vector Distance Change (%)": [f"{s:.2f}%" for s in payload['shifts']],
        "Top Text Drift Drivers": [", ".join(words) if isinstance(words, list) else "N/A" for words in true_historical_keywords]
    })
    st.dataframe(
        historical_matrix.sort_values(by="Policy Meeting Date", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={"Top Text Drift Drivers": st.column_config.TextColumn("Top Text Drift Drivers", help="Highest variance NLP elements.", width="large")}
    )

with right_panel:
    st.subheader("🕵️ Historic Window Inspector")
    reversed_dates = list(reversed(payload['dates']))
    selected_date = st.selectbox("Choose Target Policy Meeting:", reversed_dates)
    date_idx = payload['dates'].index(selected_date)
    selected_shift = payload['shifts'][date_idx]
    selected_words = true_historical_keywords[date_idx]
    
    st.markdown("---")
    st.markdown(f"📂 **Audit Profile for Meeting Statement: `{selected_date}`**")
    inner_metric_col1, inner_metric_col2 = st.columns(2)
    
    inner_metric_col1.metric("Calculated Shift", f"{selected_shift:.2f}%")
    status_label = "🚨 Breach" if selected_shift > anomaly_threshold else "✅ Stable"
    inner_metric_col2.metric("Regime Class", status_label)
    
    st.markdown("**Drift Vector Tokens:**")
    for word in selected_words:
        st.markdown(f"🔹 `{word}`")
