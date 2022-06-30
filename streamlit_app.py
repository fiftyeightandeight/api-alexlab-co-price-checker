import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
import json 
from datetime import datetime
import pytz

url = "http://api.alexlab.co/v1/price/"
token_list = [ "token-wstx", "age000-governance-token", "auto-alex", "token-wxusd", "token-wusda", "token-wbtc", "token-xbtc", "token-wban", "token-wslm", "token-wmia", "token-wnycc" ]

def safe_execute(response):
    try:
        return json.loads(response)['price']
    except Exception:
        return None

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
data['Instant (Spot)'] = instant_prices
data['Resilient (TWAP)'] = resilient_prices
data['External'] = external_prices

df = pd.DataFrame(data = data, index = token_list)
st.table(df)
st.info('Last Refreshed at ' + datetime.now(pytz.timezone('Asia/Hong_Kong')))

# with st.echo(code_location='below'):
    
