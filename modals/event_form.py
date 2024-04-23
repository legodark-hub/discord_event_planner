import datetime
import discord
from views.event_view import Event


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
                required=False,
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
            time = datetime.datetime.strptime(self.children[2].value, "%H:%M %d.%m.%Y")
        except ValueError:
            await interaction.response.send_message(
                "Формат времени должен быть ЧЧ:ММ ДД.ММ.ГГГГ", ephemeral=True
            )
            return

        if time <= datetime.datetime.now():
            await interaction.response.send_message(
                "Время сбора не может быть в прошлом", ephemeral=True
            )
            return

        participants = self.children[3].value
        if not participants.isdigit() or int(participants) <= 0:
            await interaction.response.send_message(
                "Количество участников должно быть положительным целым числом.",
                ephemeral=True,
            )
            return

        event_name = self.children[0].value
        description = self.children[1].value
        participants_needed = self.children[3].value

        event = Event(
            interaction,
            interaction.user,
            event_name,
            description,
            time,
            participants_needed,
        )
        await event.send(interaction)
