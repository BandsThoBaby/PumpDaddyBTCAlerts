# PumpDaddyBTCAlerts
PumpDaddy scans the charts so you don’t have to—BTC alerts, market signals, and momentum tracking beamed straight to your Telegram.

🚀 PumpDaddy: Your BTC Price Sentinel

PumpDaddy is a sleek, Telegram-powered BTC alert system that notifies you every time Bitcoin crosses a major price milestone ($1K intervals from $1K to $175K). Built for degens, traders, and crypto scholars who refuse to miss a signal.

🎯 Features

BTC Milestone Tracking: Alerts you at every $1,000 BTC price level

Real-Time Updates: Integrates Binance API for live price data

Telegram Bot UI: /start menu, quick commands, interactive buttons

Time-Zone Friendly: Local time + UTC timestamp included

Expandable Modules: Future-ready for whale tracking, alpha leaks, and custom signals

📷 Preview

(Coming soon: Telegram screenshots of milestone alert & menu)

🧠 Why PumpDaddy?

Designed for focus, not fluff.

Zero distractions — just actionable BTC alerts.

Build your edge. Set it. Forget it. Trade smarter.

🧰 Tech Stack

Python 3.11+

python-telegram-bot v20+

Binance API

CoinGecko (optional / deprecated for now)

📁 Project Structure

pumpdaddy/
├── main.py                # Main app hub + Telegram bot interface
├── milestone_alerts.py    # Price logic and milestone scanning
├── utils.py               # Reusable tools (coming soon)
├── whale_watch.py         # Future module (large transfers, alpha)
└── README.md              # This file

🛠 Setup Instructions

Clone the repo

git clone https://github.com/BandsThoBaby/pumpdaddy.git
cd pumpdaddy

Install dependencies

pip install -r requirements.txt

Set up your environment
Use Replit Secrets or .env file to store:

BOT_TOKEN — your Telegram Bot Token

CHAT_ID — your Telegram user ID

Run the bot

python main.py

📈 Roadmap



🧙‍♂️ Credits & License

Crafted with ❤️ by @BandsThoBaby

Open source, MIT licensed. Steal this idea. Fork it. Improve it. Just don’t rugpull.

"First it sends a ping, then it brings the pump." — PumpDaddy
