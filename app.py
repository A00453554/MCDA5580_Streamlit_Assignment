import pandas as pd
import requests
import streamlit as st

st.title("Bitcoin Prices")

list_of_currency = ['cad','usd','inr']

API_URL='https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'

no_of_days = st.slider('No of Days', min_value=1, max_value=365, value=90)
currency_selected = st.radio('Currency', list_of_currency)

payload = {'vs_currency':currency_selected,'days':str(no_of_days),'interval':'daily'}
req = requests.get(API_URL,payload)

if(req.status_code==200):
    raw_data = req.json()
    df_bitcoins = pd.DataFrame(raw_data['prices'][:-1], columns=['date',currency_selected])
    df_bitcoins['date'] = pd.to_datetime(df_bitcoins['date'], unit='ms')
    df_bitcoins.sort_values(by="date",inplace=True)
    df_bitcoins = df_bitcoins.set_index('date')
    st.line_chart(df_bitcoins)
    average_price = df_bitcoins[currency_selected].mean()
    result = "Average price during this time was "+ str(average_price)+' '+currency_selected
    st.write(result)

else:
    st.write('API has failed to fetch data.')
