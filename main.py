import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
from datetime import datetime

app = Flask('')
@app.route('/')
def home():
    return "Sol's Tracker is online!"
def run():
    app.run(host='0.0.0.0', port=8080)
Thread(target=run, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! Sol's Tracker is online!")

# MAIN COMMAND FOR ANDROID - !rolled Arcane 1000000
@bot.command()
async def rolled(ctx, *, text: str = None):
    # Usage: !rolled Arcane 1000000  OR  !rolled Lunar : Full Moon 500000
    if not text:
        await ctx.send("Use it like: `!rolled Arcane 1000000`")
        return

    # Split name and chance - last word is chance if it's a number
    parts = text.rsplit(' ', 1)
    if len(parts) == 2 and parts[1].replace(',', '').isdigit():
        aura = parts[0]
        chance = parts[1].replace(',', '')
        chance_fmt = f"{int(chance):,}"
    else:
        aura = text
        chance_fmt = "???"

    embed = discord.Embed(
        title="Roll",
        description=f"**You rolled {aura}!**\n\n**1/{chance_fmt} Chance**",
        color=0x2b2dff,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text=f"Detected | {ctx.author.display_name}")
    # Try to post in afk-events if it exists
    target = None
    if ctx.guild:
        for ch in ctx.guild.channels:
            if "afk" in ch.name.lower() and "event" in ch.name.lower():
                target = ch
                break
    if target and target != ctx.channel:
        await target.send(embed=embed)
        await ctx.send(f"✅ Logged to {target.mention}!")
    else:
        await ctx.send(embed=embed)

@bot.command()
async def biome(ctx, status: str = ""):
    status = status.lower()
    if status in ["started", "start"]:
        await ctx.send("🔴 **Rare Biome Started**")
    elif status in ["ended", "end", "ended - null"]:
        await ctx.send("⚫ **Rare Biome Ended - Null**")
    else:
        await ctx.send("Use: `!biome started` or `!biome ended`")

@bot.command()
async def help(ctx):
    await ctx.send("**Sol's Tracker - Android Commands:**\n`!rolled Arcane 1000000` - log a roll\n`!rolled Lunar : Full Moon 500000` - log a roll with name\n`!biome started` / `!biome ended` - log biome\n`!ping` - check if online")

# ALSO auto-detect if you paste "You rolled Arcane!"
@bot.event
async def on_message(message):
    if message.author == bot.user:
        await bot.process_commands(message)
        return
    content = message.content
    if content.lower().startswith("you rolled") and not content.startswith("!"):
        # Let the rolled command handle it - just copy it
        aura_text = content[10:].strip().replace("!", "")
        ctx = await bot.get_context(message)
        # Call rolled logic manually by sending embed
        embed = discord.Embed(
            title="Roll",
            description=f"**You rolled {aura_text}!**",
            color=0x2b2dff,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Detected | {message.author.display_name}")
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

bot.run(os.getenv('DISCORD_TOKEN'))
