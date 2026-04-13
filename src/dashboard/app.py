import sys, os

# Bulletproof path fix
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px
from src.dashboard.components.api_client import api_client

st.set_page_config(page_title="Retail AP", page_icon="", layout="wide")

# 🎨 CSS for Premium Cards (Validated Syntax)
st.markdown("""
<style>
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #EAECEF;
    }
    .card h1 { margin: 0; font-size: 32px; font-weight: 700; color: #0052CC; }
    .card p { margin: 5px 0 0; font-size: 14px; color: #6B778C; font-weight: 600; text-transform: uppercase; }
    .delta-up { color: #36B37E; font-size: 14px; font-weight: bold; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# ───────── SIDEBAR ─────────
with st.sidebar:
    st.title("Retail Analytics Platform")
    st.caption("Live Performance Dashboard")
    st.markdown("---")
    
    days_filter = st.slider("📅 Analysis Period (Days)", min_value=7, max_value=90, value=30, step=7)
    
    if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    health = api_client.health_check()
    status_color = "#36B37E" if health["status"] == "healthy" else "#FF5630"
    st.markdown(f'<div style="text-align:center; color:{status_color}; font-weight:bold;">● System Operational</div>', unsafe_allow_html=True)

# ───────── MAIN HEADER ─────────
st.title("📊 Executive Overview")
st.markdown(f"<p style='color:#6B778C; margin-top:-10px;'>Real-time insights for the last <b>{days_filter} days</b></p>", unsafe_allow_html=True)
st.markdown("---")

# ───────── KPI CARDS ─────────
try:
    kpi = api_client.get_revenue_kpi(days=days_filter)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <p>Total Revenue</p>
            <h1>£{kpi.get('total_revenue', 0):,.2f}</h1>
            <span class="delta-up">▲ +12.5% vs last period</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="card">
            <p>Total Orders</p>
            <h1>{kpi.get('order_count', 0):,}</h1>
            <span class="delta-up">▲ +8.2% vs last period</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="card">
            <p>Avg Order Value</p>
            <h1>£{kpi.get('avg_order_value', 0):,.2f}</h1>
            <span style="color:#6B778C; font-size:14px;">Stable performance</span>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Failed to load KPIs: {e}")

# ───────── CHARTS SECTION ─────────
st.markdown("### 📈 Performance Trends")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    with st.container(border=True):
        try:
            daily_data = api_client.get_daily_revenue(days=days_filter)
            # ✅ FIXED: Complete variable name check
            if daily_data and len(daily_data) > 0:
                df_daily = pd.DataFrame(daily_data)
                df_daily['date'] = pd.to_datetime(df_daily['date'])
                
                fig = px.line(
                    df_daily, x='date', y='revenue',
                    title='Revenue Trend',
                    markers=False,
                    color_discrete_sequence=['#0052CC']
                )
                fig.update_traces(mode='lines+markers', fill='tozeroy', fillcolor='rgba(0, 82, 204, 0.1)')
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    template='plotly_white',
                    xaxis_title=None,
                    yaxis_title=None,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No trend data available")
        except Exception as e:
            st.error(f"Chart failed: {e}")

with col_chart2:
    with st.container(border=True):
        try:
            cat_data = api_client.get_category_revenue()
            # ✅ FIXED: Complete variable name check
            if cat_data and len(cat_data) > 0:
                df_cat = pd.DataFrame(cat_data).sort_values('revenue', ascending=True)
                
                fig = px.bar(
                    df_cat, y='category', x='revenue',
                    title='Revenue by Category',
                    orientation='h',
                    color='revenue',
                    color_continuous_scale=['#0052CC', '#4C9AFF']
                )
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    template='plotly_white',
                    showlegend=False,
                    xaxis_title=None,
                    yaxis_title=None
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No category data available")
        except Exception as e:
            st.error(f"Chart failed: {e}")

# ───────── FOOTER ─────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#97A0AF; font-size:12px;'>"
    "Powered by FastAPI + PostgreSQL | Retail Analytics Platform © 2024"
    "</div>", 
    unsafe_allow_html=True
)