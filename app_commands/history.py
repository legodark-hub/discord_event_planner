import discord
from discord import app_commands
from views.history_view import HistoryView


@app_commands.guild_only()
class Commands(app_commands.Group):

    @app_commands.command(name="author", description="Созданные вами события")
    async def history_author(self, interaction: discord.Interaction):
        history_view = HistoryView(interaction.user.id, "автор")
        await history_view.send(interaction)

    @app_commands.command(
        name="participant",
        description="События, в которых вы принимали участие",
    )
    async def history_participant(self, interaction: discord.Interaction):
        history_view = HistoryView(interaction.user.id, "участник")
        await history_view.send(interaction)


async def setup(bot):
    bot.tree.add_command(
        Commands(name="event_history", description="event history commands")
    )
