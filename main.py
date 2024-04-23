import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands


intents = discord.Intents().default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
commands_dir = "app_commands"
logger = logging.getLogger("discord")


@bot.command(name="ping1", help="Responds with pong")
async def ping1(ctx):
    await ctx.send("pong")


@bot.event
async def on_ready():
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"{commands_dir}.{filename[:-3]}")
                logger.info(f"Loaded {filename}")
            except Exception as e:
                logger.error(f"Error loading {filename}: {e}")
    await bot.tree.sync()
    logger.info(f"Logged in as {bot.user}")


def main():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
