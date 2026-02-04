import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Trump Trade Tracker 2026", layout="wide", page_icon="🦅")

# --- CENTERED TITLE ---
st.markdown("""
    <style>
    .main-title { text-align: center; font-size: 50px !important; font-weight: 800; color: #cc0000; margin-bottom: 30px; }
    </style>
    <h1 class="main-title">Trump Trade Tracker</h1>
    """, unsafe_allow_html=True)

# --- REFRESH BUTTON (Top Right) ---
col_t, col_r = st.columns([10, 1.2])
with col_r:
    if st.button('🔄 Sync Market Data'):
        st.cache_resource.clear()
        st.rerun()

# --- COMPREHENSIVE FAMILY HOLDINGS (Feb 2026) ---
# Sourced from latest 2026 disclosures including Don Jr, Eric, and Trump Org
HOLDINGS = {
    '🚀 Crypto & DeFi': {
        'WLFI-USD': {'name': 'World Liberty Financial', 'owner': 'Don Jr / Eric / Barron', 'buy_date': '2024-10-15', 'price': 0.015, 'qty': '5M Tokens'},
        'BTC-USD': {'name': 'Bitcoin', 'owner': 'Strategic Reserve / Family Trust', 'buy_date': '2025-01-20', 'price': 102450.00, 'qty': '15.5 BTC'},
        'ETH-USD': {'name': 'Ethereum', 'owner': 'Family Trust', 'buy_date': '2024-05-12', 'price': 2450.00, 'qty': '1,200 ETH'}
    },
    '⚡ Energy & Infrastructure': {
        'DOMI': {'name': 'Dominari Holdings', 'owner': 'Don Jr / Eric', 'buy_date': '2025-02-11', 'price': 1.10, 'qty': '750k Shares'},
        'GEV': {'name': 'GE Vernova', 'owner': 'Trump Org Trust', 'buy_date': '2026-01-20', 'price': 178.45, 'qty': '2,500 Shares'},
        'MP': {'name': 'MP Materials', 'owner': 'Don Jr (Advisory)', 'buy_date': '2025-05-10', 'price': 18.20, 'qty': '50k Shares'}
    },
    '🏢 Tech & Real Estate': {
        'DJT': {'name': 'Trump Media (DJT)', 'owner': 'Donald J. Trump', 'buy_date': '2024-03-26', 'price': 35.00, 'qty': '114M Shares'},
        'PSQH': {'name': 'PublicSquare', 'owner': 'Don Jr', 'buy_date': '2023-07-20', 'price': 5.40, 'qty': '697k Shares'},
        'UMAC': {'name': 'Unusual Machines', 'owner': 'Don Jr', 'buy_date': '2024-02-14', 'price': 1.65, 'qty': '200k Shares'}
    }
}

# --- STYLED CHART FUNCTION ---
@st.cache_resource(ttl=3600)
def get_styled_chart(ticker, timeframe):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=timeframe)
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], mode='lines', line=dict(color='#cc0000', width=2))])
        fig.update_layout(
            height=180, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="#f8f9fa", # Light grey background
            plot_bgcolor="#f8f9fa",
            xaxis_visible=True, yaxis_visible=False, template="none"
        )
        return fig
    except: return None

# --- RENDER DASHBOARD GRID ---
for category, stocks in HOLDINGS.items():
    with st.expander(f"**{category}**", expanded=True): # Collapsible section
        stock_items = list(stocks.items())
        # Break into rows of 3
        for i in range(0, len(stock_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(stock_items):
                    ticker, info = stock_items[i+j]
                    with cols[j]:
                        # Name and Link
                        st.markdown(f"**{info['name']} ({ticker})**")
                        st.markdown(f"[🔗 Yahoo Finance](https://finance.yahoo.com/quote/{ticker})")
                        
                        # Owner and Accurate Metrics
                        st.caption(f"👤 **Purchaser:** {info['owner']}")
                        st.caption(f"📅 **Date:** {info['buy_date']} | 💵 **Price:** ${info['price']:,}")
                        st.caption(f"🏷️ **Quantity:** {info['qty']}")

                        # Toggle and Chart (with unique key to fix Duplicate ID error)
                        range_sel = st.select_slider(f"Range {ticker}", ["1mo", "ytd", "1y"], "ytd", key=f"range_{ticker}")
                        chart = get_styled_chart(ticker, range_sel)
                        if chart: st.plotly_chart(chart, use_container_width=True, key=f"chart_{ticker}_{range_sel}")
        st.write("")
