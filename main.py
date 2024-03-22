import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents().all()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.command(name="ping1", help="Responds with pong")
async def ping1(ctx):
    await ctx.send("pong")

@bot.event
async def on_ready():
    await bot.load_extension("bot.test_commands")
    await bot.load_extension("bot.event")
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")


if __name__ == "__main__":
    bot.run(TOKEN)
