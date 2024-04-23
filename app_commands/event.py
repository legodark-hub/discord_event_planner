import datetime
import discord
from discord import app_commands
from views.event_view import Event
from modals.event_form import EventForm


class Commands(app_commands.Group):
    @app_commands.command(name="create_event", description="Создание нового события")
    async def create_event(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EventForm())

    @app_commands.command(name="test_event", description="тест события")
    async def test_event(self, interaction: discord.Interaction):
        event = Event(
            interaction,
            interaction.user,
            "Тестовое событие",
            "Тестовое описание",
            datetime.datetime.now() + datetime.timedelta(minutes=30),
            5,
        )
        await event.send(interaction)


async def setup(bot):
    bot.tree.add_command(Commands(name="event", description="event commands"))
