# Load libraries
import requests
import pandas as pd
import numpy as np
import streamlit as st

# Select Coin
selectCoin = st.sidebar.radio(
    "Choose Coin",
    ("Bitcoin", "Ethereum")
)

if selectCoin == "Bitcoin":
    coinid = "bitcoin"
else:
    coinid = "ethereum"
 
# Selection Currency
chooseCurr = st.sidebar.radio(
    "Choose Currency",
    ("CAD", "USD","INR")
)

if chooseCurr == "CAD":
    curr = "cad"
elif chooseCurr == "INR":
    curr = "inr"
else:
    curr = "usd"

curr = curr.upper()

st.title(coinid.title()+" Daily Prices")

days = st.slider("Number of Days:",1,365, 31,1)

payload = {'vs_currency': curr, 'days': days, 'interval':'daily'}

r = requests.get(f'https://api.coingecko.com/api/v3/coins/{coinid}/market_chart'
                 , params=payload)

price_list = r.json()['prices']

df = pd.DataFrame(price_list[:len(price_list)-1], 
                  columns =['Date', curr]) 

df.Date = pd.to_datetime(df.Date, unit='ms')
df[curr] = df[curr].apply(lambda p : round(p,0))

df.set_index(df.Date, inplace=True)
df.drop('Date',axis=1,inplace=True)

st.line_chart(df, use_container_width = True)

periodStart = df.head(1).index[0].date().strftime('%m/%d/%Y')
periodEnd = df.tail(1).index[0].date().strftime('%m/%d/%Y')

st.subheader(f"Some Insights during {periodStart} to {periodEnd}:")

st.text(f"Average Price is {np.round(np.mean(df[curr]),2)} {curr}")
st.text(f"Maximum Price is {np.round(np.max(df[curr]),2)} {curr}")