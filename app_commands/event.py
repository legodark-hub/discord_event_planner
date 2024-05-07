import datetime
import discord
from discord import app_commands
from views.event_view import Event
from modals.event_form import EventForm
from views.history_view import HistoryView


@app_commands.guild_only()
class Commands(app_commands.Group):
    @app_commands.command(name="create_event", description="Создание нового события")
    async def create_event(self, interaction: discord.Interaction):
        event_form = EventForm()
        await interaction.response.send_modal(event_form)


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

    @app_commands.command(name="history_author", description="Созданные вами события")
    async def history_author(self, interaction: discord.Interaction):
        history_view = HistoryView(interaction.user.id, "автор")
        await history_view.send(interaction)

    @app_commands.command(
        name="history_participant",
        description="События, в которых вы принимали участие",
    )
    async def history_participant(self, interaction: discord.Interaction):
        history_view = HistoryView(interaction.user.id, "участник")
        await history_view.send(interaction)

async def setup(bot):
    bot.tree.add_command(Commands(name="event", description="event commands"))
