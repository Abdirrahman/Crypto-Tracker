import os
import requests as req
from datetime import datetime, timezone, timedelta
import time
import json
from rich.console import Console
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import numpy as np
import pandas as pd

CRYPTO = "ethereum"
INTERVAL = "d1"
START = "1448064000000"
END = datetime.now().timestamp() * 1000
PREVIOUS_MONTH = (datetime.now() - timedelta(days=31)).timestamp() * 1000

console = Console()


def unix_converter():
    '''Converts datetime into unix format'''
    date = datetime(2023, 5, 1)

    return time.mktime(date.timetuple())


def get_training_data(auth_token: str, crypto: str = CRYPTO, interval: str = INTERVAL, start: str = START, end: str = PREVIOUS_MONTH) -> dict[list, str]:
    '''Retrieves ETH data from the start date to last month'''
    url = f"https://api.coincap.io/v2/assets/{crypto}/history?interval={interval}&start={start}&end={end}"

    headers = {"X-CoinAPI-Key": auth_token}

    r = req.request("GET", url, headers=headers)

    return r.json()

def get_prediction_data(auth_token: str, crypto: str = CRYPTO, interval: str = INTERVAL, start: str = PREVIOUS_MONTH, end: str = END) -> dict[list, str]:
    '''Retrieves ETH data from past month'''
    url = f"https://api.coincap.io/v2/assets/{crypto}/history?interval={interval}&start={start}&end={end}"

    headers = {"X-CoinAPI-Key": auth_token}

    r = req.request("GET", url, headers=headers)

    return r.json()
