from flask import Flask
import threading
import time
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


def bot():
    while True:
        try:
            url = "https://api.twelvedata.com/time_series"

            params = {
                "symbol": "EUR/USD",
                "interval": "5min",
                "apikey": API_KEY
            }

            r = requests.get(url)

            print(r.json())

        except Exception as e:
            print(e)

        time.sleep(60)


@app.route("/")
def home():
    return "Forex Algo Bot Running"


threading.Thread(target=bot, daemon=True).start()

port = int(os.getenv("PORT", 10000))

app.run(
    host="0.0.0.0",
    port=port
)
