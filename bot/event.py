import datetime
import discord
from discord import Button, ButtonStyle, app_commands


class Commands(app_commands.Group):
    @app_commands.command(name="create_event", description="Создание нового события")
    async def create_event(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EventForm())

    @app_commands.command(name="test_event", description="тест события")
    async def test_event(self, interaction: discord.Interaction):
        await event_message(interaction, "Тестовое событие", "Тестовое описание", datetime.datetime.now(), 5)


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
                label="Время сбора (ЧЧ:ММ ДД.ММ.ГГГГ)",
                placeholder="Введите время сбора (ЧЧ:ММ ДД.ММ.ГГГГ)...",
                min_length=16,
                max_length=19,
                required=True,
            )
        )
        self.add_item(
            discord.ui.TextInput(
                label="Количество участников (кроме вас)",
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

        # await interaction.response.send_message(
        #     f"Название события: {self.children[0].value}\n"
        #     f"Описание: {self.children[1].value}\n"
        #     f"Время сбора: {self.children[2].value}\n"
        #     f"Количество участников: {self.children[3].value}"
        # )

        event_name = self.children[0].value
        description = self.children[1].value
        time = self.children[2].value
        participants_needed = self.children[3].value

        await event_message(interaction, event_name, description, time, participants_needed)



async def event_message(interaction: discord.Interaction, event_name, description, time, participants_needed, participant = None):
    participants = []
    embed = discord.Embed(
        title=event_name,
        description=description,
    )
    embed.add_field(name="Время сбора:", value=time, inline=True)
    embed.add_field(name="Нужно участников:", value=participants_needed, inline=True)
    embed.add_field(name=f"Запросил:", value=interaction.user.mention, inline=True)
    embed.add_field(name="Записались:", value="\n".join(participants), inline=False)
    await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(Commands(name="event", description="event commands"))
