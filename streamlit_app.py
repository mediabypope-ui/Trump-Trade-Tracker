import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Trump Trade Tracker 2026", layout="wide", page_icon="🦅")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- TRACKED INVESTMENTS DATA ---
# Update this list whenever they make a new move!
INVESTMENTS = {
    'UMAC': {'name': 'Unusual Machines', 'type': 'Defense/Drones', 'date': '2024-02-14', 'note': 'Don Jr. Advisory Board'},
    'DOMI': {'name': 'Dominari Holdings', 'type': 'AI Energy', 'date': '2025-11-01', 'note': 'Strategic AI Pivot'},
    'PSQH': {'name': 'PublicSquare', 'type': 'Marketplace', 'date': '2023-07-20', 'note': 'Parallel Economy Play'},
    'GEV': {'name': 'GE Vernova', 'type': 'Energy Grid', 'date': '2026-01-20', 'note': 'Natural Gas Expansion Beneficiary'},
    'MP': {'name': 'MP Materials', 'type': 'Rare Earths', 'date': '2025-05-10', 'note': 'Critical Mineral Security'}
}

# --- SIDEBAR ---
st.sidebar.title("🦅 Tracker Settings")
selected_ticker = st.sidebar.selectbox("Choose a Stock to View", list(INVESTMENTS.keys()))
chart_period = st.sidebar.radio("Chart Timeframe", ["1 Month", "Year-To-Date (YTD)"])

# --- DATA FETCHING ---
@st.cache_data(ttl=3600)  # Refresh every hour
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    # Map selection to yfinance periods
    period_map = {"1 Month": "1mo", "Year-To-Date (YTD)": "ytd"}
    hist = stock.history(period=period_map[chart_period])
    info = stock.fast_info
    return hist, info

try:
    hist, info = get_stock_data(selected_ticker)
    curr_price = info['last_price']
    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else curr_price
    delta = ((curr_price - prev_close) / prev_close) * 100

    # --- HEADER ---
    st.title(f"{INVESTMENTS[selected_ticker]['name']} ({selected_ticker})")
    st.write(f"**Strategic Note:** {INVESTMENTS[selected_ticker]['note']}")

    # --- TOP METRICS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${curr_price:.2f}", f"{delta:.2f}%")
    col2.metric("Investment Date", INVESTMENTS[selected_ticker]['date'])
    col3.metric("Sector", INVESTMENTS[selected_ticker]['type'])

    # --- CHARTING ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index, 
        y=hist['Close'], 
        mode='lines+markers',
        name='Price',
        line=dict(color='#cc0000', width=3),
        fill='toself',
        fillcolor='rgba(204, 0, 0, 0.1)'
    ))
    fig.update_layout(
        title=f"{selected_ticker} {chart_period} Price Action",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- FOOTER LINKS ---
    st.divider()
    y_link = f"https://finance.yahoo.com/quote/{selected_ticker}"
    st.markdown(f"🔗 [Open {selected_ticker} on Yahoo Finance]({y_link})")

except Exception as e:
    st.error(f"Could not load data for {selected_ticker}. Error: {e}")
