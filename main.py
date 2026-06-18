import os
import time
import requests
import pandas as pd

API_KEY = os.getenv("API_KEY")

SYMBOL = "EUR/USD"
INTERVAL = "5min"

def get_data():
    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "outputsize": 100,
        "apikey": API_KEY
    }

    r = requests.get(url)
    data = r.json()

    candles = data["values"]
    df = pd.DataFrame(candles)

    df["close"] = df["close"].astype(float)

    return df.iloc[::-1]


def strategy(df):
    df["ema20"] = df["close"].ewm(span=20).mean()
    df["ema50"] = df["close"].ewm(span=50).mean()

    last = df.iloc[-1]

    if last["ema20"] > last["ema50"]:
        return "BUY"

    return "SELL"


while True:
    try:
        df = get_data()

        signal = strategy(df)

        print("Signal:", signal)

        time.sleep(60)

    except Exception as e:
        print(e)
        time.sleep(30)
