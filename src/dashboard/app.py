import sys
import os

# Fix Streamlit path issue
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from src.dashboard.components.api_client import api_client

st.set_page_config(
    page_title="🛍️ Retail Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("🛍️ Retail Analytics")
    st.markdown("---")
    
    # Date Range Filter
    st.markdown("### 📅 Date Range")
    days_filter = st.slider("Days to show", 7, 90, 30)
    
    if st.button("🔄 Refresh Data"):
        api_client.get_revenue_kpi.cache_clear()
        st.rerun()
    
    st.markdown("---")
    
    # API Health Check
    health = api_client.health_check()
    if health["status"] == "healthy":
        st.success("✅ API Connected")
    else:
        st.error("❌ API Disconnected")
        st.stop()

# Main Page
st.title("📊 Executive Summary")
st.markdown(f"*Real-time retail performance insights - Last {days_filter} days*")
st.markdown("---")

# Fetch KPIs
kpi_data = api_client.get_revenue_kpi(days=days_filter)

# KPI Cards Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💷 Total Revenue",
        value=f"£{kpi_data['total_revenue']:,.2f}",
        delta=f"{kpi_data.get('growth', '+0.0')}%"
    )

with col2:
    st.metric(
        label="🛒 Total Orders",
        value=f"{kpi_data['order_count']:,}",
        delta=f"{kpi_data.get('order_growth', '+0.0')}%"
    )

with col3:
    st.metric(
        label="🎯 Avg Order Value",
        value=f"£{kpi_data['avg_order_value']:.2f}",
        delta=None
    )

with col4:
    st.metric(
        label="👥 Unique Customers",
        value=f"{kpi_data.get('unique_customers', 0):,}",
        delta=None
    )

st.markdown("---")

# Charts Section
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Revenue Trend (Last 30 Days)")
    # Placeholder - will replace with real API endpoint
    dates = pd.date_range(end=datetime.now(), periods=30)
    revenue_data = pd.DataFrame({
        'date': dates,
        'revenue': [kpi_data['total_revenue']/30 * (0.8 + 0.4*i/30) for i in range(30)]
    })
    fig_trend = px.line(
        revenue_data, 
        x='date', 
        y='revenue',
        title='Daily Revenue'
    )
    fig_trend.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_trend, use_container_width=True)

with col_chart2:
    st.subheader("🔥 Top Categories")
    # Placeholder data
    categories = ['Electronics', 'Apparel', 'Home & Garden', 'Sports', 'Books']
    cat_data = pd.DataFrame({
        'category': categories,
        'revenue': [kpi_data['total_revenue']*0.35, kpi_data['total_revenue']*0.25, 
                   kpi_data['total_revenue']*0.20, kpi_data['total_revenue']*0.12,
                   kpi_data['total_revenue']*0.08]
    })
    fig_cat = px.bar(
        cat_data,
        x='category',
        y='revenue',
        color='revenue',
        color_continuous_scale='Blues'
    )
    fig_cat.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_cat, use_container_width=True)

# Insights Section
st.markdown("---")
st.subheader("💡 Key Insights")
col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.info("""
    **📊 Performance Summary:**
    - Revenue is trending upward
    - Average order value is stable
    - Customer retention is healthy
    """)

with col_insight2:
    st.warning("""
    **💡 Recommendations:**
    - Focus on high-value categories
    - Implement upselling strategies
    - Monitor inventory levels
    """)