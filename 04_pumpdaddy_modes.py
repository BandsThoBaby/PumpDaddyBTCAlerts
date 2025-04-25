            # === pumpdaddy_modes.py ===
            # Modular logic to support user alert mode preferences

            import time
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
            from telegram.ext import ContextTypes, CallbackQueryHandler

            # === In-memory user state (swap with DB later) ===
            user_settings = {}

            # === Mode Labels with Emojis ===
            mode_names = {
                "turbo": "⚡ Turbo",
                "analyst": "📊 Analyst",
                "allin": "🧠 All-In"
            }
            ALERT_MODES = list(mode_names.keys())

            # === Set mode for a user ===
            def set_user_mode(user_id, mode):
                if mode not in ALERT_MODES:
                    return False
                user_settings[user_id] = user_settings.get(user_id, {})
                user_settings[user_id]["mode"] = mode
                user_settings[user_id]["last_alert_time"] = 0
                user_settings[user_id]["last_price"] = 0
                user_settings[user_id]["last_milestone"] = 0
                return True

            # === Should we alert this user based on their mode ===
            def should_alert(user_id, price, milestone):
                now = time.time()
                user = user_settings.get(user_id, {})
                mode = user.get("mode", "turbo")
                last_time = user.get("last_alert_time", 0)
                last_price = user.get("last_price", 0)
                last_milestone = user.get("last_milestone", 0)

                if mode == "turbo":
                    return now - last_time >= 60

                elif mode == "analyst":
                    price_change_pct = abs(price - last_price) / last_price * 100 if last_price else 0
                    return (now - last_time >= 600 and price_change_pct >= 3) or milestone >= last_milestone + 2000

                elif mode == "allin":
                    return True

                return False

            # === Update state after alert sent ===
            def update_user_state(user_id, price, milestone):
                now = time.time()
                user_settings[user_id]["last_alert_time"] = now
                user_settings[user_id]["last_price"] = price
                user_settings[user_id]["last_milestone"] = milestone

            # === Show inline mode selection menu ===
            async def show_alert_mode_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
                keyboard = [
                    [InlineKeyboardButton(label, callback_data=f"set_mode_{key}")]
                    for key, label in mode_names.items()
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    "🧠 Choose your alert style:",
                    reply_markup=reply_markup
                )

            # === Handle mode button clicks ===
            async def alert_mode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
                query = update.callback_query
                await query.answer()
                user_id = query.from_user.id

                if query.data.startswith("set_mode_"):
                    mode = query.data.replace("set_mode_", "")
                    if set_user_mode(user_id, mode):
                        await query.edit_message_text(
                            f"✅ Alert mode set to: *{mode_names[mode]}*",
                            parse_mode="Markdown"
                        )
                    else:
                        await query.edit_message_text("❌ Invalid alert mode.")

            # === Register callback handler with app ===
            def register_alert_mode_handlers(app):
                app.add_handler(CallbackQueryHandler(alert_mode_callback, pattern="^set_mode_"))