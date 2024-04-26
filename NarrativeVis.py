import streamlit as st
import pandas as pd
import altair as alt
import calendar

# Enable data transformer for Altair
alt.data_transformers.enable("default")

df = pd.read_csv("./MarketData.csv")

# Data preprocessing
df['Date'] = pd.to_datetime(df['Date'])
df['Price_Change'] = df['Adj Close'] - df['Open']
df['Price_Change_Direction'] = df['Price_Change'].apply(lambda x: 1 if x > 0 else 0)
df['Price_Percentage_Change'] = ((df['Close'] - df['Open']) / df['Open']) * 100
df['Price_Percentage_Change_Direction'] = df['Price_Percentage_Change'].apply(lambda x: 1 if x > 0 else 0)
window_size = 5
df['Moving_Average'] = df['Adj Close'].rolling(window=window_size).mean()
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Month'].apply(lambda x: calendar.month_name[x])

ticker_name_mapping = {
    '^NYA': 'New York Stock Exchange',
    '^IXIC': 'NASDAQ',
    '^DJI': 'Dow Jones',
    '^GSPC': 'S&P 500'
}

df['Ticker_Name'] = df['Ticker'].map(ticker_name_mapping)
months_order = [calendar.month_name[i] for i in range(1, 13)]

# Streamlit UI elements
year = st.selectbox('Select a Year:', options=df['Year'].unique())

# Filtering data based on selected year
filtered_df = df[df['Year'] == year]

# Create the chart
chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Month_Name:O", title="Month", sort=months_order, axis=alt.Axis(labelAngle=-45)),
    xOffset=alt.XOffset("Ticker:N", title="Ticker"),
    y=alt.Y("sum(Volume):Q", title="Total Volume"),
    color=alt.Color("Ticker_Name:N", title="Ticker"),
    tooltip=[alt.Tooltip('sum(Volume):Q', title="Volume Sum", format=',.0f')]
).properties(
    title="Monthly Volume Sum for Each Ticker in Selected Year"
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
