import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Investment Tracker 2026", layout="wide", page_icon="📈")

# --- THE WATCHLIST ---
INVESTMENTS = {
    'UMAC': {'name': 'Unusual Machines', 'note': 'Don Jr. Advisory Board'},
    'DOMI': {'name': 'Dominari Holdings', 'note': 'AI Energy Pivot'},
    'PSQH': {'name': 'PublicSquare', 'note': 'Parallel Economy Marketplace'},
    'GEV': {'name': 'GE Vernova', 'note': 'Natural Gas Infrastructure'},
    'DJT': {'name': 'Trump Media', 'note': 'Truth Social / Crypto Expansion'}
}

# --- DATA FETCHING (Fixed Caching) ---
# We use cache_resource for complex objects like Tickers
@st.cache_resource(ttl=3600)
def get_ticker_object(ticker_symbol):
    return yf.Ticker(ticker_symbol)

st.title("🦅 Live Portfolio Dashboard")

# --- SIDEBAR CONTROLS ---
selected_ticker = st.sidebar.selectbox("Select Investment", list(INVESTMENTS.keys()))
# We define time_frame here so it's available for the rest of the app
time_frame = st.sidebar.radio("Timeframe", ["1mo", "ytd", "1y"])

# --- PROCESS DATA ---
try:
    stock = get_ticker_object(selected_ticker)
    hist = stock.history(period=time_frame)
    
    # Simple dictionary for the price to avoid serialization errors
    curr_price = stock.fast_info['last_price']

    # --- DISPLAY METRICS ---
    st.header(f"{INVESTMENTS[selected_ticker]['name']} ({selected_ticker})")
    c1, c2 = st.columns([2, 1])

    with c1:
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index, 
            open=hist['Open'], 
            high=hist['High'], 
            low=hist['Low'], 
            close=hist['Close']
        )])
        fig.update_layout(title=f"{selected_ticker} {time_frame.upper()} Chart", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.metric("Current Price", f"${curr_price:.2f}")
        st.write(f"**Strategic Goal:** {INVESTMENTS[selected_ticker]['note']}")
        st.markdown(f"**[View on Yahoo Finance](https://finance.yahoo.com/quote/{selected_ticker})**")

    # --- NEWS FEED ---
    st.divider()
    st.subheader(f"📰 Latest News for {selected_ticker}")
    news_list = stock.news
    if news_list:
        for article in news_list[:5]:
            st.markdown(f"**[{article['title']}]({article['link']})**")
            st.caption(f"Source: {article.get('publisher', 'Unknown')}")
    else:
        st.write("No recent headlines found.")

except Exception as e:
    st.error(f"Error loading data for {selected_ticker}: {e}")
