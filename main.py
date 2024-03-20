import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands


load_dotenv()  # Loads the env variables from .env file
TOKEN = os.getenv("DISCORD_BOT_SECRET")  # Fetching token from env variable

intents = discord.Intents().all()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


# @bot.command(name="hello", help="Responds with a greeting")
# async def hello(ctx):
#     await ctx.send(f"Hello, {ctx.message.author.mention}")


@tree.command(name="hello", description="Responds with a greeting")
async def hello(interaction):
    await interaction.response.send_message(
        content="Секретное сообщение", ephemeral=True
    )


@bot.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {bot.user}")


if __name__ == "__main__":
    bot.run(TOKEN)
