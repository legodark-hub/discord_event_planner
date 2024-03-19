import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()  # Loads the env variables from .env file
TOKEN = os.getenv("DISCORD_BOT_SECRET")  # Fetching token from env variable

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command(name="hello", help="Responds with a greeting")
async def hello(ctx):
    await ctx.send('Hello, {0.author.mention}'.format(ctx.message))

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

if __name__ == "__main__":
    bot.run(TOKEN)
