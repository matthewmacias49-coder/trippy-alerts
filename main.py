import discord
from discord.ext import tasks

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 123456789012345678

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    daily_watchlist.start()

@tasks.loop(hours=24)
async def daily_watchlist():
    channel = client.get_channel(CHANNEL_ID)

    if channel:
        await channel.send("""
📈 WATCHLIST

🔥 AMD
🔥 NVDA
🔥 PLTR
🔥 HOOD
🔥 SLV

👀 INTC
👀 TSLA
👀 WBD
        """)

client.run(TOKEN)
