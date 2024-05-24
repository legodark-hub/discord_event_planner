import discord
from discord import app_commands
from modals.event_form import EventForm


@app_commands.guild_only()
class Commands(app_commands.Group):
    @app_commands.command(name="create_event", description="Создание нового события")
    async def create_event(self, interaction: discord.Interaction):
        event_form = EventForm()
        await interaction.response.send_modal(event_form)

async def setup(bot):
    bot.tree.add_command(Commands(name="event", description="event commands"))
