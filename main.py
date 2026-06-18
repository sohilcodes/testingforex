from flask import Flask
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():

    token = os.getenv("OANDA_API_KEY","").strip()
    account = os.getenv("ACCOUNT_ID","").strip()

    return {
        "token_exists": bool(token),
        "account_exists": bool(account),
        "account": account[-6:] if account else "missing"
    }

app.run(
host="0.0.0.0",
port=int(os.getenv("PORT",10000))
)
