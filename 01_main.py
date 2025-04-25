import os
import asyncio
import nest_asyncio
import requests
from datetime import datetime
import pytz

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

    # Replit async fix
nest_asyncio.apply()

    # === Bot config ===
bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']
symbol = "BTCUSDT"
milestones = list(range(1000, 175001, 1000))  # Every $1K from $1K to $175K
check_interval = 30  # seconds
triggered = set()


    # === Price Fetch ===
def get_price():
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        return float(response.json()['price'])


    # === Message Builder ===
def format_message(price, milestone, last_milestone):
        now_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        bangkok = pytz.timezone('Asia/Bangkok')
        now_local = datetime.now(bangkok).strftime('%H:%M:%S (Bangkok, GMT+7)')

        pct_change = ((price - last_milestone) / last_milestone) * 100 if last_milestone else 0

        return (
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 BTC Milestone Crossed: ${milestone:,}\n\n"
            f"💰 Current Price: ${price:,.2f}\n"
            f"📈 Up {pct_change:.2f}% from ${last_milestone:,}\n\n"
            f"🕒 Time (UTC): {now_utc}\n"
            f"🗺 Local Time: {now_local}\n\n"
            f"📉 Chart: https://tradingview.com/symbols/BTCUSD/\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )


    # === /start command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        menu = [["📈 Track BTC", "🧠 Milestones"], ["❓ Help", "🔧 Settings"]]
        reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
        await update.message.reply_text(
            "🚀 Welcome to PumpDaddy — your BTC price sentinel.\n\nChoose an option below 👇",
            reply_markup=reply_markup
        )


    # === /help command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "PumpDaddy alerts you when BTC hits milestones, tracks whales, and whispers alpha.\n\n"
            "Use the buttons or type /start to return to the main menu."
        )


    # === Price Monitor ===
async def monitor_loop(app):
        await app.bot.send_message(chat_id=chat_id, text="🎩 PumpDaddy scanning BTC Price milestones every $1K to the Moon! 🚀🌕")
        while True:
            try:
                price = get_price()
                print(f"📈 BTC Price: ${price}")
                for milestone in milestones:
                    if milestone <= price and milestone not in triggered:
                        last_milestone = milestone - 1000 if milestone > 1000 else 0
                        message = format_message(price, milestone, last_milestone)
                        await app.bot.send_message(chat_id=chat_id, text=message)
                        triggered.add(milestone)
            except Exception as e:
                print("❌ Error:", e)
            await asyncio.sleep(check_interval)


    # === Main runner ===
async def main():
        print("👔 PumpDaddy is live — Telegram UI + Milestone Monitor activated.")
        app = ApplicationBuilder().token(bot_token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        asyncio.create_task(monitor_loop(app))
        await app.run_polling()


    # === Launch PumpDaddy ===
asyncio.get_event_loop().run_until_complete(main())