from flask import Flask
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("OANDA_API_KEY")
ACCOUNT = os.getenv("ACCOUNT_ID")


@app.route("/")
def home():

    if not TOKEN or not ACCOUNT:
        return {
            "status": "missing_env"
        }

    url = (
        f"https://api-fxpractice.oanda.com/v3/accounts/{ACCOUNT}"
    )

    headers = {
        "Authorization":
        f"Bearer {TOKEN}"
    }

    try:

        r = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        data = r.json()

        if r.status_code == 200:

            account = data["account"]

            return {
                "connected": True,
                "currency": account["currency"],
                "balance": account["balance"]
            }

        return data

    except Exception as e:

        return {
            "error": str(e)
        }


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                10000
            )
        )
    )
