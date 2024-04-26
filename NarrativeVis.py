import pandas as pd
import altair as alt
import calendar

alt.data_transformers.enable("vegafusion")

df = pd.read_csv("~/Documents/MarketData/MarketData.csv")

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

# Apply the mapping
df['Ticker_Name'] = df['Ticker'].map(ticker_name_mapping)

months_order = [calendar.month_name[i] for i in range(1, 13)]

### Radio Button for Years
# Years 2008 - 2023
years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
labels = [str(year) + ' ' for year in years]

input_dropdown = alt.binding_radio(
    options=years,
    labels=labels,
    name='Year: '
)

selection = alt.selection_point(
    fields=['Year'],
    bind=input_dropdown,
)

# Now create the chart
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("Month_Name:O", title="Month",
            sort=months_order,
            axis=alt.Axis(labelAngle=-45)),
    xOffset=alt.XOffset("Ticker:N", title="Ticker"),
    y=alt.Y("sum(Volume):Q", title="Total Volume"),
    color=alt.Color("Ticker_Name:N", title="Ticker"),
    tooltip=[alt.Tooltip('sum(Volume):Q', title="Volume Sum", format=',.0f')]
).properties(
    title="Monthly Volume Sum for Each Ticker in Selected Year"
).add_params(
    selection
).transform_filter(
    selection
)

chart.show()
