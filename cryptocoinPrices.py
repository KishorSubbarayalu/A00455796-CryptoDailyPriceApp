# Load libraries
import requests
import pandas as pd
import numpy as np
from datetime import datetime
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

st.title(coinid.title()+" Daily Prices"+f" in {curr.upper()}")

days = st.slider("Number of Days:",1,365, 31,1)

payload = {'vs_currency': curr, 'days': days, 'interval':'daily'}

r = requests.get(f'https://api.coingecko.com/api/v3/coins/{coinid}/market_chart'
                 , params=payload)

price_list = r.json()['prices']

df = pd.DataFrame(price_list[:len(price_list)-1], 
                  columns =['Date', 'Price']) 

df.Date = df.Date.apply(lambda t : datetime.utcfromtimestamp(t/1000).date())
df.Price = df.Price.apply(lambda p : round(p,0))

df.set_index(df.Date, inplace=True)
df.drop('Date',axis=1,inplace=True)

st.line_chart(df, use_container_width = True)

st.subheader(f"Some Insights during {df.head(1).index[0]} to {df.tail(1).index[0]}:")

st.text(f"Average Price was {np.round(np.mean(df.Price),2)} {curr.upper()}")

maxPriceDay = df[df.Price == np.max(df.Price)].index[0]

st.text(f"Maximum Price: {np.round(np.max(df.Price),2)}, was sold on {maxPriceDay}")