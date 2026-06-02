import discord
from discord.ext import tasks
import os
import yfinance as yf
from datetime import datetime
import pytz

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 1449119042458878081

WATCHLIST_POOL = [
    "SMH",
    "AMZN",
    "HOOD",
    "TSLA",
    "DAL",
    "UAL",
    "AAL",
    "LLY",
    "IBM",
    "GOOG",
    "AMD",
    "DELL",
    "ADM",
    "DE",
    "NFLX",
    "INTC",
    "NBIS",
    "MSFT",
    "PLTR",
    "CL=F",
    "META",
    "USO",
    "SLV",
    "IAU",
    "SPY",
    "CVX",
    "COP",
    "VLO",
    "XLE",
    "XOM",
    "LMT",
    "WBD",
    "SI=F",
    "INSM",
    "NVDA"
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

                movers.append((symbol, pct_change))

        except Exception as e:
            print(f"Error with {symbol}: {e}")
            continue

    movers.sort(key=lambda x: abs(x[1]), reverse=True)

    return movers[:5]


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    try:
        channel = await client.fetch_channel(CHANNEL_ID)

        if channel:
            await channel.send("✅ Trippy Alerts Online")

    except Exception as e:
        print(f"Channel error: {e}")

    if not daily_watchlist.is_running():
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

        try:
            channel = await client.fetch_channel(CHANNEL_ID)

            movers = get_top_movers()

            today_str = now.strftime("%B %d, %Y")

            if not movers:
                await channel.send(
                    f"📈 **TRIPPY MATT WATCHLIST — {today_str}**\n\nNo significant movers found."
                )
                return

            biggest = movers[0]

            message = f"📈 **TRIPPY MATT WATCHLIST — {today_str}**\n\n"

            for symbol, pct in movers:
                emoji = "🚀" if pct > 0 else "🔻"
                message += f"{emoji} **{symbol}** ({pct:+.2f}%)\n"

            message += f"\n🔥 **Biggest Mover:** {biggest[0]} ({biggest[1]:+.2f}%)"

            message += "\n\n🎯 **Why They're On Watch**"
            message += "\n• Top 5 movers from my personal watchlist"
            message += "\n• Looking for momentum continuation and breakout setups"
            message += "\n• Watching for unusual movement and trader attention"
            message += "\n• Strong movers often create the best day-trade opportunities"
            message += "\n• These are the stocks most likely to be on my radar today"

            await channel.send(message)

        except Exception as e:
            print(f"Watchlist error: {e}")


client.run(TOKEN)
