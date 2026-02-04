import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Trump Trade Tracker", layout="wide", page_icon="🦅")

# --- CUSTOM CSS FOR CENTERED TITLE ---
st.markdown("""
    <style>
    .centered-title { text-align: center; font-size: 50px !important; font-weight: 800; color: #cc0000; margin-bottom: 30px; }
    </style>
    <h1 class="centered-title">Trump Trade Tracker</h1>
    """, unsafe_allow_html=True)

# --- DETAILED INVESTMENT DATA ---
# Categories: 'Crypto', 'Energy', 'Tech', 'Real Estate'
INVESTMENTS = {
    'Energy': {
        'DOMI': {'name': 'Dominari Holdings', 'buy_date': '2025-11-01', 'shares': 500, 'buy_price': 4.50},
        'GEV': {'name': 'GE Vernova', 'buy_date': '2026-01-20', 'shares': 100, 'buy_price': 175.20}
    },
    'Tech/Media': {
        'DJT': {'name': 'Trump Media', 'buy_date': '2024-03-26', 'shares': 1000, 'buy_price': 35.00},
        'UMAC': {'name': 'Unusual Machines', 'buy_date': '2024-02-14', 'shares': 250, 'buy_price': 2.10}
    },
    'Marketplace': {
        'PSQH': {'name': 'PublicSquare', 'buy_date': '2023-07-20', 'shares': 300, 'buy_price': 5.40}
    }
}

# --- CHARTING FUNCTION ---
def create_chart(ticker_symbol, timeframe):
    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(period=timeframe)
    fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], mode='lines', line=dict(color='#cc0000'))])
    fig.update_layout(
        height=250, margin=dict(l=0, r=0, t=30, b=0),
        title=f"{ticker_symbol} ({timeframe.upper()})",
        template="plotly_white",
        xaxis_rangeslider_visible=False
    )
    return fig

# --- MAIN DASHBOARD LAYOUT ---
for category, stocks in INVESTMENTS.items():
    st.header(f"📂 Category: {category}")
    cols = st.columns(3) # Creates a row of 3 columns
    
    for i, (ticker, details) in enumerate(stocks.items()):
        with cols[i % 3]: # Places charts in rows of 3
            # Timeframe Toggle inside the chart row
            view = st.radio(f"Period ({ticker})", ["1mo", "ytd", "1y"], key=f"range_{ticker}", horizontal=True)
            
            # Display the Chart
            st.plotly_chart(create_chart(ticker, view), use_container_width=True)
            
            # Display Purchase Data
            st.info(f"**Purchased:** {details['buy_date']}\n\n**Price:** ${details['buy_price']} | **Shares:** {details['shares']}")
    st.divider()
