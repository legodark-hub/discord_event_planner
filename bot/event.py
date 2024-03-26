import datetime
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
                required=True,
            )
        )
        self.add_item(
            discord.ui.TextInput(
                label="Описание",
                placeholder="Введите описание...",
                style=discord.TextStyle.paragraph,
                max_length=300,
            )
        )
        self.add_item(
            discord.ui.TextInput(
                label="Время сбора",
                placeholder="Введите время сбора (ЧЧ:ММ ДД.ММ.ГГГГ)...",
                min_length=16,
                max_length=19,
                required=True,
            )
        )
        self.add_item(
            discord.ui.TextInput(
                label="Количество участников",
                placeholder="Введите количество участников...",
                min_length=1,
                max_length=2,
                required=True,
            )
        )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            datetime.datetime.strptime(self.children[2].value, "%H:%M %d.%m.%Y")
        except ValueError:
            await interaction.response.send_message(
                "Формат времени должен быть ЧЧ:ММ ДД.ММ.ГГГГ", ephemeral=True
            )
            return

        participants = self.children[3].value
        if not participants.isdigit() or int(participants) <= 0:
            await interaction.response.send_message(
                "Количество участников должно быть положительным целым числом.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Название события: {self.children[0].value}\n"
            f"Описание: {self.children[1].value}\n"
            f"Время сбора: {self.children[2].value}\n"
            f"Количество участников: {self.children[3].value}"
        )


async def setup(bot):
    bot.tree.add_command(Commands(name="event", description="event commands"))
