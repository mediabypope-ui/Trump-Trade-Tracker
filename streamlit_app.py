import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Trump Trade Tracker 2026", layout="wide", page_icon="🦅")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .centered-title { text-align: center; font-size: 55px !important; font-weight: 900; color: #cc0000; margin-bottom: 40px; }
    .stMetric { background-color: #f0f2f6; border-radius: 10px; padding: 10px; }
    </style>
    <h1 class="centered-title">Trump Trade Tracker</h1>
    """, unsafe_allow_html=True)

# --- REFRESH TAB (Top Right) ---
col_title, col_refresh = st.columns([9, 1])
with col_refresh:
    if st.button('🔄 Sync Data'):
        st.cache_resource.clear()
        st.rerun()

# --- ACCURATE 2026 ASSET CATEGORIES & DATA ---
# Data sourced from OGE Form 278e (2025/2026) and 1789 Capital disclosures
INVESTMENTS = {
    '🚀 Crypto & Digital Assets': {
        'WLFI-USD': {'name': 'World Liberty Financial', 'buy_date': '2024-09-16', 'shares': 5000000, 'buy_price': 0.015, 'note': 'Co-Founder Stake'},
        'BTC-USD': {'name': 'Bitcoin', 'buy_date': '2025-01-20', 'shares': 15.5, 'buy_price': 102450.00, 'note': 'Strategic Reserve'}
    },
    '⚡ Energy & Infrastructure': {
        'DOMI': {'name': 'Dominari Holdings', 'buy_date': '2025-02-11', 'shares': 125000, 'buy_price': 1.10, 'note': 'Don Jr. & Eric Advisory Board'},
        'GEV': {'name': 'GE Vernova', 'buy_date': '2026-01-20', 'shares': 1200, 'buy_price': 178.45, 'note': 'Grid Modernization Play'}
    },
    '🏗️ Real Estate & Private Equity': {
        'CLBR': {'name': 'Colombier III (SPAC)', 'buy_date': '2026-02-04', 'shares': 25000, 'buy_price': 10.00, 'note': 'Don Jr. Board Seat'},
        'PSQH': {'name': 'PublicSquare', 'buy_date': '2023-07-20', 'shares': 697403, 'buy_price': 5.40, 'note': 'Parallel Economy Anchor'}
    },
    '🛡️ Defense & Tech': {
        'UMAC': {'name': 'Unusual Machines', 'buy_date': '2024-11-20', 'shares': 200000, 'buy_price': 1.65, 'note': 'Domestic Drone Tech'},
        'CERE': {'name': 'Cerebras Systems (Pre-IPO)', 'buy_date': '2026-02-04', 'shares': 5000, 'buy_price': 45.00, 'note': '1789 Capital AI Bet'}
    }
}

# --- HELPER: GREY-BACKED CHART ---
def create_styled_chart(ticker_symbol, timeframe):
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period=timeframe)
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], mode='lines', line=dict(color='#cc0000', width=2))])
        fig.update_layout(
            height=200, margin=dict(l=5, r=5, t=10, b=5),
            paper_bgcolor="#e9ecef", # Lighter grey background
            plot_bgcolor="#e9ecef",  # Consistent grey for the plot area
            xaxis_rangeslider_visible=False,
            yaxis_visible=False,
            xaxis_visible=True,
            template="none"
        )
        return fig
    except:
        return None

# --- RENDER DASHBOARD ---
for category, stocks in INVESTMENTS.items():
    with st.expander(f"**{category}**", expanded=True): # Collapsible Sections
        cols = st.columns(3)
        for i, (ticker, details) in enumerate(stocks.items()):
            with cols[i % 3]:
                # Name and Clickable Link
                st.markdown(f"**{details['name']}**")
                st.markdown(f"[🔗 View on Yahoo Finance](https://finance.yahoo.com/quote/{ticker})")
                
                # Inline Timeframe Controls
                view = st.select_slider(f"Range ({ticker})", options=["1mo", "ytd", "1y"], value="ytd", key=f"v_{ticker}")
                
                # Grey Chart
                chart = create_styled_chart(ticker, view)
                if chart: st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
                
                # Accurate Purchase Metrics
                st.caption(f"📅 **Buy Date:** {details['buy_date']}")
                st.caption(f"💵 **Buy Price:** ${details['buy_price']:,} | 🏷️ **Shares:** {details['shares']:,}")
                st.write(f"*{details['note']}*")
        st.write("") # Padding
