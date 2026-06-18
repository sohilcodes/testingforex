import asyncio
import logging
import os
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from strategy import check_signal
from trader import place_order, get_open_trades, close_all_trades
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, PAIRS

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

EMOJI = {"BUY": "🟢", "SELL": "🔴", "HOLD": "⏸️"}


async def send_message(text: str):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Telegram error: {e}")


async def run_strategy():
    logger.info("🔍 Checking signals...")
    for pair in PAIRS:
        try:
            signal, rsi, price = check_signal(pair)
            emoji = EMOJI.get(signal, "⏸️")
            logger.info(f"{pair}: {signal} | RSI={rsi:.1f} | Price={price}")

            if signal in ["BUY", "SELL"]:
                result = place_order(pair, signal)

                if result["status"] == "success":
                    msg = (
                        f"{emoji} <b>TRADE PLACED</b>\n\n"
                        f"📌 Pair: <b>{pair}</b>\n"
                        f"📊 Action: <b>{signal}</b>\n"
                        f"💰 Price: <b>{price:.5f}</b>\n"
                        f"📈 RSI: <b>{rsi:.1f}</b>\n"
                        f"📦 Units: <b>{result['units']}</b>\n"
                        f"🛑 Stop Loss: <b>{result['sl']:.5f}</b>\n"
                        f"🎯 Take Profit: <b>{result['tp']:.5f}</b>\n"
                        f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}"
                    )
                    await send_message(msg)
                else:
                    await send_message(f"⚠️ Order failed for {pair}: {result['error']}")

        except Exception as e:
            logger.error(f"Error processing {pair}: {e}")
            await send_message(f"❌ Error on {pair}: {str(e)}")


async def send_status():
    try:
        trades = get_open_trades()
        if not trades:
            await send_message("📭 <b>Open Trades:</b> None")
            return

        msg = "📋 <b>Open Trades Status</b>\n\n"
        for t in trades:
            pl_emoji = "🟢" if float(t["pl"]) >= 0 else "🔴"
            msg += (
                f"{pl_emoji} {t['instrument']}\n"
                f"   Side: {t['side']} | Units: {t['units']}\n"
                f"   P/L: {t['pl']} | Price: {t['price']}\n\n"
            )
        await send_message(msg)
    except Exception as e:
        logger.error(f"Status error: {e}")


async def main():
    await send_message(
        "🤖 <b>Forex Auto Trading Bot Started!</b>\n\n"
        f"📌 Pairs: {', '.join(PAIRS)}\n"
        f"⏱️ Strategy: RSI (14) — 15min candles\n"
        f"🔁 Check interval: Every 15 minutes\n\n"
        "Bot is now monitoring the market..."
    )

    scheduler = AsyncIOScheduler()

    # Strategy check — har 15 min
    scheduler.add_job(run_strategy, "interval", minutes=15, id="strategy")

    # Status update — har 1 ghante
    scheduler.add_job(send_status, "interval", hours=1, id="status")

    scheduler.start()
    logger.info("✅ Scheduler started")

    # Turant ek baar check karo
    await run_strategy()

    # Bot chalta rahe
    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
            
