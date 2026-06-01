import discord
from discord.ext import tasks
import os

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 1449119042458878081

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("✅ Bot is online and connected!")

    daily_watchlist.start()
@tasks.loop(hours=24)
async def daily_watchlist():
    channel = client.get_channel(CHANNEL_ID)

    if channel:
        await channel.send("""
📈 WATCHLIST

🔥 AMD
🔥 PLTR
🔥 HOOD
""")

client.run(TOKEN)
