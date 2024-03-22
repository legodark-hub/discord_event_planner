import discord
from discord import app_commands


class Commands(app_commands.Group):
    @app_commands.command(name="create_event", description="Создание нового события")
    async def create_event(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EventForm())


class EventForm(discord.ui.Modal, title="Новое событие"):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.TextInput(
                label="Название события",
                placeholder="Введите название события...",
                min_length=1,
                max_length=100,
            )
        )
        self.add_item(
            discord.ui.TextInput(
                label="Описание",
                placeholder="Введите описание...",
                style=discord.TextStyle.paragraph,
            )
        )
        self.add_item(
            discord.ui.TextInput(
                label="Время сбора",
                placeholder="Введите время сбора...",
                min_length=1,
                max_length=100,
            )
        )
        self.add_item(
            discord.ui.TextInput(
                label="Количество участников",
                placeholder="Введите количество участников...",
                min_length=1,
                max_length=100,
            )
        )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Название события: {self.children[0].value}\nОписание: {self.children[1].value}\nВремя сбора: {self.children[2].value}\nКоличество участников: {self.children[3].value}",
            ephemeral=True,
        )


async def setup(bot):
    bot.tree.add_command(Commands(name="event", description="event commands"))
