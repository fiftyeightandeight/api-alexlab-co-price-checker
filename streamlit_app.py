from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
import json 

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
url = "http://api.alexlab.co/v1/price/"
token_list = [ "token-wstx", "age000-governance-token", "token-wxusd", "token-wbtc", "token-wusda", "token-wban", "token-wslm", "token-wmia", "token-wnycc", "auto-alex" ]

def safe_execute(response):
    try:
        return json.loads(response)['price']
    except Exception:
        return -1

with st.echo(code_location='below'):

    instant_prices = []
    resilient_prices = []
    external_prices = []
    for x in token_list:
        res = requests.get(url + x)
        instant_prices.append(safe_execute(res.text))
        res = requests.get(url + x + '-twap')
        resilient_prices.append(safe_execute(res.text))
        res = requests.get(url + x + '-external')
        external_prices.append(safe_execute(res.text))
    
    data = {}
    data['Spot'] = instant_prices
    data['TWAP'] = resilient_prices
    data['External'] = external_prices

    df = pd.DataFrame(data = data, index = token_list)

    st.dataframe(df)
