import requests as req
import datetime as dt
from rich.console import Console
from dotenv import load_dotenv
import os
import plotly.express as px
import pandas as pd

CRYPTO = "ethereum"
INTERVAL = "d1"
START = "1448064000000"
END = dt.datetime.now().timestamp() * 1000

console = Console()


def millis_to_datetime(millis: int):
    date = dt.datetime.fromtimestamp(millis/1000.0, tz=dt.timezone.utc)
    return date


def datetime_to_millis(date):
    epoch = dt.datetime.utcfromtimestamp(0)
    delta = date - epoch
    return int(delta.total_seconds() * 1000)


def get_crypto_data(auth_token: str, crypto: str = CRYPTO, interval: str = INTERVAL, start: str = START, end: str = END) -> dict[list, str]:

    url = f"https://api.coincap.io/v2/assets/{crypto}/history?interval={interval}&start={start}&end={end}"

    headers = {"X-CoinAPI-Key": auth_token}

    r = req.request("GET", url, headers=headers)

    return r.json()


def capitalize_words(sentence):
    words = sentence.split(" ")
    capitalized_words = [word.capitalize() for word in words]
    capitalized_sentence = " ".join(capitalized_words)
    return capitalized_sentence


def get_crypto_graph(start, end, crypto):
    response = get_crypto_data(
        auth_token=os.environ['api_key'], start=start, end=end, crypto=crypto)
    date = millis_to_datetime(response['timestamp'])
    data = response["data"]
    df = pd.DataFrame(data)
    df['priceUsd'] = df['priceUsd'].astype(float)
    df['time'] = df['time'].apply(lambda x: millis_to_datetime(x))
    fig = px.line(df, x='time', y='priceUsd', labels={
        'time': 'Date', 'priceUsd': 'Price (USD)'})

    fig.update_layout(title={"text": f"{capitalize_words(crypto)} Graph", "x": 0.5,
                      "y": 0.9, "xanchor": "center", "yanchor": "middle"})

    return fig


def get_crypto_list():
    url = f"https://api.coincap.io/v2/assets"
    r = req.request("GET", url).json()
    val = [{'label': crypto['name'], 'value': crypto['id']}
           for crypto in r['data']]
    return val
