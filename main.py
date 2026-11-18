import discord
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Sol's Tracker is online!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    if msg == "!ping":
        await message.channel.send("Pong! Sol's Tracker is online!")
    elif msg == "!help":
        await message.channel.send("**Commands:**\n`!ping` - check if I'm online\n`!track` - check for open sports")
    elif msg == "!track":
        await message.channel.send("🔍 Scanning... No open sports detected right now.")

client.run(os.environ['TOKEN'])
