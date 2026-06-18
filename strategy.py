import pandas as pd
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
from config import OANDA_API_KEY, OANDA_ENV, RSI_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT, CANDLE_COUNT, GRANULARITY

client = oandapyV20.API(access_token=OANDA_API_KEY, environment=OANDA_ENV)


def get_candles(pair: str) -> pd.DataFrame:
    params = {"granularity": GRANULARITY, "count": CANDLE_COUNT}
    r = instruments.InstrumentsCandles(instrument=pair, params=params)
    client.request(r)

    candles = r.response["candles"]
    data = []
    for c in candles:
        if c["complete"]:
            data.append({
                "open":  float(c["mid"]["o"]),
                "high":  float(c["mid"]["h"]),
                "low":   float(c["mid"]["l"]),
                "close": float(c["mid"]["c"]),
            })

    return pd.DataFrame(data)


def calculate_rsi(df: pd.DataFrame, period: int = RSI_PERIOD) -> pd.Series:
    delta = df["close"].diff()
    gain  = delta.where(delta > 0, 0.0)
    loss  = -delta.where(delta < 0, 0.0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs  = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def check_signal(pair: str) -> tuple[str, float, float]:
    """
    Returns (signal, rsi_value, current_price)
    signal: "BUY" | "SELL" | "HOLD"
    """
    df    = get_candles(pair)
    df["rsi"] = calculate_rsi(df)

    rsi           = df["rsi"].iloc[-1]
    current_price = df["close"].iloc[-1]
    prev_rsi      = df["rsi"].iloc[-2]

    # RSI crossover confirmation (false signal filter)
    if prev_rsi < RSI_OVERSOLD and rsi >= RSI_OVERSOLD:
        signal = "BUY"
    elif prev_rsi > RSI_OVERBOUGHT and rsi <= RSI_OVERBOUGHT:
        signal = "SELL"
    else:
        signal = "HOLD"

    return signal, rsi, current_price
  
