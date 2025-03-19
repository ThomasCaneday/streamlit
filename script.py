import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set page configuration for a wide layout and custom title.
st.set_page_config(page_title="Financial Time Series Analysis", layout="wide")

st.title("Financial Time Series Analysis")
st.markdown("This app simulates a financial time series and performs a basic analysis. Adjust the parameters in the sidebar to update the simulation.")

# Sidebar for simulation parameters
st.sidebar.header("Simulation Settings")
start_price = st.sidebar.number_input("Starting Price", value=100.0, step=1.0)
days = st.sidebar.slider("Number of Trading Days", min_value=100, max_value=500, value=252, step=1)
volatility = st.sidebar.slider("Daily Volatility (%)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
ma_window = st.sidebar.slider("Moving Average Window", min_value=5, max_value=30, value=10, step=1)

# Generate date range for business days
dates = pd.bdate_range(start=pd.Timestamp.today() - pd.Timedelta(days=days*2), periods=days)

# Simulate daily returns using a normal distribution and compute price as a random walk
np.random.seed(42)
daily_returns = np.random.normal(loc=0, scale=volatility/100, size=len(dates))
price = start_price * np.exp(np.cumsum(daily_returns))

# Create DataFrame with the simulated price data
df = pd.DataFrame({
    "Date": dates,
    "Price": price
})
df.set_index("Date", inplace=True)

# Calculate the moving average
df["Moving_Avg"] = df["Price"].rolling(window=ma_window).mean()

# Reset index for Altair compatibility
chart_data = df.reset_index()

# Time series chart: Stock price and moving average
st.subheader("Stock Price & Moving Average")
price_chart = alt.Chart(chart_data).mark_line().encode(
    x=alt.X("Date:T", title="Date"),
    y=alt.Y("Price:Q", title="Price"),
    tooltip=["Date:T", "Price:Q"]
).properties(width=800, height=400)

ma_chart = alt.Chart(chart_data).mark_line(color="orange").encode(
    x="Date:T",
    y=alt.Y("Moving_Avg:Q", title="Moving Average"),
    tooltip=["Date:T", "Moving_Avg:Q"]
)

combined_chart = price_chart + ma_chart
st.altair_chart(combined_chart, use_container_width=True)

# Calculate daily percentage returns and add as a new column
df["Daily_Return"] = df["Price"].pct_change()

# Histogram of daily returns
st.subheader("Histogram of Daily Returns")
hist_chart = alt.Chart(df.reset_index()).mark_bar().encode(
    x=alt.X("Daily_Return:Q", bin=alt.Bin(maxbins=50), title="Daily Return"),
    y=alt.Y("count()", title="Frequency")
).properties(width=800, height=400)
st.altair_chart(hist_chart, use_container_width=True)

# Display a sample of the simulated data
st.subheader("Simulated Data Sample")
st.write(df.head())
