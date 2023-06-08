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
START = "1448064000000"
END = dt.datetime.now().timestamp() * 1000

console = Console()


def millis_to_datetime(millis: int):
    date = dt.datetime.fromtimestamp(millis/1000.0, tz=dt.timezone.utc)
    return date


def get_crypto_data(auth_token: str, crypto: str = CRYPTO, interval: str = INTERVAL, start: str = START, end: str = END) -> dict[list, str]:

    url = f"https://api.coincap.io/v2/assets/{crypto}/history?interval={interval}&start={start}&end={end}"

    headers = {"X-CoinAPI-Key": auth_token}

    r = req.request("GET", url, headers=headers)

    return r.json()


if __name__ == "__main__":
    # prerequisites
    load_dotenv()

    # getting data
    response = get_crypto_data(auth_token=os.environ['api_key'])
    date = millis_to_datetime(response['timestamp'])
    data = response["data"]

    console.print(data)

    # plotting graph
    df = pd.DataFrame(data)
    df['priceUsd'] = df['priceUsd'].astype(float)
    df['time'] = df['time'].apply(lambda x: millis_to_datetime(x))
    fig = px.line(df, x='time', y='priceUsd', labels={
        'time': 'Date', 'priceUsd': 'Price (USD)'})
    fig.show()
