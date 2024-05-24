import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands



intents = discord.Intents().default()
bot = commands.Bot(command_prefix="$", intents=intents)
commands_dir = "app_commands"
logger = logging.getLogger("discord")


@bot.command(name="reload", help="reload all commands", hidden=True)
@commands.is_owner()
async def reload(ctx):
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.reload_extension(f"{commands_dir}.{filename[:-3]}")
                logger.info(f"Reloaded {filename}")
            except Exception as e:
                logger.error(f"Error reloading {filename}: {e}")


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

# TODO: черный список
# TODO: настройка для отдельного сервера

def main():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
