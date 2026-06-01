import discord
from discord.ext import tasks
import os
import yfinance as yf
from datetime import datetime
import pytz

TOKEN = os.getenv(“BOT_TOKEN”)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 1449119042458878081

WATCHLIST_POOL = [
“AMD”,“NVDA”,“TSLA”,“HOOD”,“PLTR”,“MSFT”,“AMZN”,“META”,
“GOOG”,“NFLX”,“INTC”,“DELL”,“WBD”,“NBIS”,“SMH”,
“SLV”,“USO”,“XOM”,“CVX”,“COP”,
“DAL”,“UAL”,“AAL”,
“SUPV”,“ALLT”,“LUMN”,“XPEV”,
“IBM”,“LLY”,“LMT”
]

last_post_date = None

def get_top_movers():
movers = []

for symbol in WATCHLIST_POOL:
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="2d")

        if len(hist) >= 2:
            prev_close = hist["Close"].iloc[-2]
            current_close = hist["Close"].iloc[-1]

            pct_change = ((current_close - prev_close) / prev_close) * 100

            if abs(pct_change) >= 3:
                movers.append((symbol, pct_change))

    except Exception:
        continue

movers.sort(key=lambda x: abs(x[1]), reverse=True)
return movers[:5]
@client.event
async def on_ready():
print(f”Logged in as {client.user}”)

channel = await client.fetch_channel(CHANNEL_ID)

if channel:
    await channel.send("✅ Trippy Alerts Online")

daily_watchlist.start()
@tasks.loop(minutes=1)
async def daily_watchlist():
global last_post_date

pst = pytz.timezone("America/Los_Angeles")
now = datetime.now(pst)

if now.hour == 6 and now.minute == 0:

    today = now.date()

    if last_post_date == today:
        return

    last_post_date = today

    channel = await client.fetch_channel(CHANNEL_ID)

    movers = get_top_movers()

    if not movers:
        message = "📈 **TODAY'S WATCHLIST**\n\nNo stocks moved more than 3%."
    else:
        message = "📈 **TODAY'S WATCHLIST**\n\n"

        for symbol, pct in movers:
            message += f"🔥 {symbol} ({pct:+.2f}%)\n"

    await channel.send(message)
client.run(TOKEN)

