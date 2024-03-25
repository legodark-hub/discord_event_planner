import discord
from discord import app_commands

class Commands(app_commands.Group):

    @app_commands.command(name="ping", description="ping")
    async def ping(self, interaction):
        await interaction.response.send_message(content="pong", ephemeral=True)

    @app_commands.command(name="hello", description="Responds with a greeting")
    async def hello(self, interaction):
        await interaction.response.send_message(content=f"Привет, {interaction.user.mention}!", ephemeral=True)


async def setup(bot):
    bot.tree.add_command(Commands(name="commands", description="My custom commands"))
