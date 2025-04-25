from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from pumpdaddy_modes import show_alert_mode_menu, register_alert_mode_handlers, user_settings, mode_names
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_settings:
        from pumpdaddy_modes import set_user_mode
        set_user_mode(user_id, "turbo")
    current_mode = user_settings.get(user_id, {}).get("mode", "turbo")

    menu = [
        ["📈 Track BTC", "🧠 Milestones"],
        ["❓ Help", "🔧 Settings"],
        ["🧠 Alert Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)

    await update.message.reply_text(
        f"🚀 Welcome to PumpDaddy — your BTC price sentinel.\n\n"
        f"🧠 Current Alert Mode: {mode_names[current_mode]}\n\n"
        f"Choose an option below 👇",
        reply_markup=reply_markup
    )

# === /help Command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "PumpDaddy alerts you when BTC hits milestones, tracks whales, and whispers alpha.\n\n"
        "Use the buttons or type /start to return to the main menu."
    )

# === Menu Button Responses ===
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if user_input == "📈 Track BTC":
        await update.message.reply_text("Tracking enabled. You’ll get alerts when BTC hits big numbers 💸")
    elif user_input == "🧠 Milestones":
        await update.message.reply_text("Next milestone alert coming up when BTC crosses a new $1K mark.")
    elif user_input == "❓ Help":
        await help_command(update, context)
    elif user_input == "🔧 Settings":
        await update.message.reply_text("Settings will be available soon. Sit tight 😎")
    else:
        await update.message.reply_text("Sorry, I didn’t understand that. Try /start to see the menu again.")

# === Attach All Handlers ===
def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))

    # Existing settings menu (🔧 Settings)
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🔧 Settings"), settings_menu))
    app.add_handler(CallbackQueryHandler(button_callback))

    # NEW: Alert Mode menu (🧠 Alert Settings)
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🧠 Alert Settings"), show_alert_mode_menu))
    register_alert_mode_handlers(app)

# === Inline Settings Menu ===
async def settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🔔 Set Alerts", callback_data="set_alerts"),
            InlineKeyboardButton("🔕 Mute Alerts", callback_data="mute_alerts")
        ],
        [
            InlineKeyboardButton("📊 Milestone Range", callback_data="range_settings"),
            InlineKeyboardButton("❌ Close", callback_data="close_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your settings:", reply_markup=reply_markup)

# === Callback Query Handler ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "set_alerts":
        await query.edit_message_text("✅ Alerts enabled. PumpDaddy will ping you every $1K.")
    elif query.data == "mute_alerts":
        await query.edit_message_text("🔕 Alerts muted. You’ll still be able to use commands.")
    elif query.data == "range_settings":
        await query.edit_message_text("⚙️ Milestone range selection coming soon.")
    elif query.data == "close_menu":
        await query.edit_message_text("Menu closed 👌")