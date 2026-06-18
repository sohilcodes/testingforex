import os

# ── Telegram ──────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]

# ── OANDA ─────────────────────────────────────────────
OANDA_API_KEY    = os.environ["OANDA_API_KEY"]
OANDA_ACCOUNT_ID = os.environ["OANDA_ACCOUNT_ID"]
OANDA_ENV        = os.environ.get("OANDA_ENV", "practice")   # "practice" ya "live"

# ── Trading Pairs ──────────────────────────────────────
PAIRS = ["EUR_USD", "GBP_USD", "USD_JPY"]

# ── Risk Settings ──────────────────────────────────────
UNITS = {
    "EUR_USD": 1000,   # micro lot
    "GBP_USD": 1000,
    "USD_JPY": 1000,
}

SL_PIPS = 20    # Stop Loss — 20 pips
TP_PIPS = 40    # Take Profit — 40 pips (1:2 RR ratio)

# ── Strategy Settings ──────────────────────────────────
RSI_PERIOD     = 14
RSI_OVERSOLD   = 30    # BUY signal
RSI_OVERBOUGHT = 70    # SELL signal
CANDLE_COUNT   = 50    # Kitne candles fetch karne hain
GRANULARITY    = "M15" # 15-minute candles
