import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_kpi_card(title: str, value: str, delta: str = None, icon: str = "📊"):
    """Create a styled KPI card (returns HTML)"""
    delta_html = f'<p style="color: {"green" if "+" in delta else "red"}; font-size: 14px;">{delta}</p>' if delta else ""
    return f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; text-align: center;">
        <h2 style="margin: 0; font-size: 32px;">{icon}</h2>
        <p style="margin: 10px 0; font-size: 14px; opacity: 0.9;">{title}</p>
        <h1 style="margin: 5px 0; font-size: 28px;">{value}</h1>
        {delta_html}
    </div>
    """

def create_revenue_trend_chart(daily_data: pd.DataFrame):
    """Create revenue over time line chart"""
    fig = px.line(
        daily_data, 
        x="date", 
        y="revenue",
        title="📈 Revenue Trend (Last 30 Days)",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue (£)",
        hovermode="x unified",
        height=400
    )
    return fig

def create_category_bar_chart(category_data: pd.DataFrame):
    """Create category revenue bar chart"""
    fig = px.bar(
        category_data,
        x="category",
        y="revenue",
        title="🔥 Revenue by Category",
        color="revenue",
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Revenue (£)",
        height=400
    )
    return fig