import datetime
import discord
from discord import app_commands

from views.event_view import Event

class Commands(app_commands.Group):

    @app_commands.command(name="ping", description="ping")
    async def ping(self, interaction):
        await interaction.response.send_message(content="pong", ephemeral=True)

    @app_commands.command(name="hello", description="Responds with a greeting")
    async def hello(self, interaction):
        await interaction.response.send_message(content=f"Привет, {interaction.user.mention}!", ephemeral=True)
        
    @app_commands.command(name="test_event", description="тест события")
    async def test_event(self, interaction: discord.Interaction):
        event = Event(
            interaction,
            interaction.user,
            "Тестовое событие",
            "Тестовое описание",
            datetime.datetime.now() + datetime.timedelta(minutes=1),
            5,
        )
        await event.send()


async def setup(bot):
    bot.tree.add_command(Commands(name="commands", description="My custom commands"))
