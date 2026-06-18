import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades_ep
from config import OANDA_API_KEY, OANDA_ACCOUNT_ID, OANDA_ENV, UNITS, SL_PIPS, TP_PIPS

client = oandapyV20.API(access_token=OANDA_API_KEY, environment=OANDA_ENV)

# Pip value per instrument
PIP_SIZE = {
    "EUR_USD": 0.0001,
    "GBP_USD": 0.0001,
    "USD_JPY": 0.01,
}


def calculate_sl_tp(pair: str, action: str, price: float) -> tuple[float, float]:
    pip = PIP_SIZE.get(pair, 0.0001)
    sl_distance = SL_PIPS * pip
    tp_distance = TP_PIPS * pip

    if action == "BUY":
        sl = round(price - sl_distance, 5)
        tp = round(price + tp_distance, 5)
    else:  # SELL
        sl = round(price + sl_distance, 5)
        tp = round(price - tp_distance, 5)

    return sl, tp


def place_order(pair: str, action: str) -> dict:
    try:
        units     = UNITS.get(pair, 1000)
        pip       = PIP_SIZE.get(pair, 0.0001)

        # Current price fetch karo order se
        from strategy import get_candles
        df    = get_candles(pair)
        price = df["close"].iloc[-1]

        sl, tp = calculate_sl_tp(pair, action, price)

        # SELL ke liye units negative hoti hain
        if action == "SELL":
            units = -units

        order_data = {
            "order": {
                "type":        "MARKET",
                "instrument":  pair,
                "units":       str(units),
                "timeInForce": "FOK",
                "stopLossOnFill": {
                    "price": str(sl)
                },
                "takeProfitOnFill": {
                    "price": str(tp)
                },
            }
        }

        r = orders.OrderCreate(accountID=OANDA_ACCOUNT_ID, data=order_data)
        client.request(r)

        return {
            "status": "success",
            "units":  abs(units),
            "sl":     sl,
            "tp":     tp,
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_open_trades() -> list:
    try:
        r = trades_ep.OpenTrades(accountID=OANDA_ACCOUNT_ID)
        client.request(r)

        result = []
        for t in r.response.get("trades", []):
            result.append({
                "instrument": t["instrument"],
                "side":       "BUY" if float(t["currentUnits"]) > 0 else "SELL",
                "units":      abs(int(float(t["currentUnits"]))),
                "price":      t["price"],
                "pl":         t.get("unrealizedPL", "0"),
            })
        return result

    except Exception as e:
        return []


def close_all_trades() -> int:
    """Saari open trades band karo — emergency use"""
    open_trades = get_open_trades()
    closed = 0
    try:
        r = trades_ep.OpenTrades(accountID=OANDA_ACCOUNT_ID)
        client.request(r)
        for t in r.response.get("trades", []):
            trade_id = t["id"]
            close_r  = trades_ep.TradeClose(accountID=OANDA_ACCOUNT_ID, tradeID=trade_id)
            client.request(close_r)
            closed += 1
    except Exception:
        pass
    return closed
      
