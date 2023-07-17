import requests as req
import datetime as dt
import json
from rich.console import Console
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth
import plotly.express as px
import numpy as np
import pandas as pd

CRYPTO = "ethereum"
INTERVAL = "d1"
START = 1448064000000
END = str(dt.datetime.now().timestamp() * 1000)

console = Console()


def millis_to_datetime(millis: int):
    date = dt.datetime.fromtimestamp(millis/1000.0, tz=dt.timezone.utc)
    return date


def get_crypto_data(auth_token: str, crypto: str = CRYPTO, interval: str = INTERVAL, start: str = START, end: str = END) -> dict[list, str]:

    url = f"https://api.coincap.io/v2/assets/{crypto}/history?interval={interval}&start={start}&end={end}"

    headers = {"X-CoinAPI-Key": auth_token}

    r = req.request("GET", url, headers=headers)

    return r.json()


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
    return fig


if __name__ == "__main__":
    # prerequisites
    load_dotenv()

    # getting data
    fig = get_crypto_graph(START, END, CRYPTO)

    fig.show()
