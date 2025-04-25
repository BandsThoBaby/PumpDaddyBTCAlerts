        import requests
        import asyncio
        from datetime import datetime
        import pytz
        import os
        import time

        # === Config ===
        symbol = "BTCUSDT"
        check_interval = 30  # seconds
        milestones = list(range(1000, 175001, 1000))
        chat_id = os.environ['CHAT_ID']

        # === Cooldown settings ===
        ALERT_COOLDOWN_SECONDS = 180  # 3 minutes

        # === User state ===
        user_settings = {}

        # === Get price from Binance ===
        def get_price():
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(url)
            return float(response.json()['price'])

        # === Get latest milestone crossed ===

        def get_latest_milestone_crossed(last_price, current_price, milestones):
            """
            Returns only the highest milestone crossed between last_price and current_price.
            """
            crossed = [m for m in milestones if last_price < m <= current_price]
            return max(crossed) if crossed else None

        # === Format alert message ===
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

        # === Initialize user state on join/startup ===
        def init_user_state(user_id, current_price):
            user_settings[user_id] = {
                "mode": "analyst",  # default mode
                "last_price": current_price,
                "last_milestone": get_latest_milestone_crossed(0, current_price) or 0,
                "last_alert_time": time.time()
            }

        # === Smart alert logic ===
        def should_send_alert(user_id, milestone, current_price):
            now = time.time()
            user_data = user_settings.get(user_id, {})
            last_milestone = user_data.get("last_milestone", 0)
            last_alert_time = user_data.get("last_alert_time", 0)
            user_mode = user_data.get("mode", "analyst")

            crossed_multiple = (milestone - last_milestone) >= 2000
            cooldown_expired = (now - last_alert_time) > ALERT_COOLDOWN_SECONDS
            turbo_mode = user_mode == "turbo"

            if milestone and should_send_alert(chat_id, milestone, price):
                last_milestone = user_data.get("last_milestone", milestone - 1000)
                message = format_message(price, milestone, last_milestone)
                await app.bot.send_message(chat_id=chat_id, text=message)
                user_data["last_price"] = current_price
                user_settings[user_id] = user_data
                return True

            return False

        # === Main monitoring loop ===
# === Main monitoring loop ===
        async def monitor_loop(app):
            await app.bot.send_message(chat_id=chat_id, text="🎩 PumpDaddy scanning BTC milestones from $1K to $175K! 🚀")
        
            price = get_price()
            init_user_state(chat_id, price)
        
            while True:
                try:
                    price = get_price()
                    user_data = user_settings.get(chat_id, {})
        
                    print(f"[INFO] BTC ${price:,.2f} — Checking milestones crossed...")
                    print(f"[DEBUG] User Mode: {user_data.get('mode')} | Last Alert: {int(time.time() - user_data.get('last_alert_time', 0))}s ago")
        
                    last_price = user_data.get("last_price", 0)
                    milestone = get_latest_milestone_crossed(last_price, price)
                    print(f"🧠 Checking: last_price={last_price} → current_price={price} | crossed={milestone}")
        
                    # ✅ Always update last_price to avoid rechecking same range
                    user_data["last_price"] = price
                    user_settings[chat_id] = user_data
        
                    if milestone and should_send_alert(chat_id, milestone, price):
                        last_milestone = user_data.get("last_milestone", milestone - 1000)
                        message = format_message(price, milestone, last_milestone)
                        await app.bot.send_message(chat_id=chat_id, text=message)
        
                except Exception as e:
                    print("❌ Error:", e)
        
                await asyncio.sleep(check_interval)