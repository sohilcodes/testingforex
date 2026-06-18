from flask import Flask
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("OANDA_API_KEY", "").strip()
ACCOUNT = os.getenv("ACCOUNT_ID", "").strip()


@app.route("/")
def home():

    url = f"https://api-fxpractice.oanda.com/v3/accounts/{ACCOUNT}/summary"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.get(
        url,
        headers=headers
    )

    return r.text


app.run(
    host="0.0.0.0",
    port=int(
        os.getenv(
            "PORT",
            10000
        )
    )
)
