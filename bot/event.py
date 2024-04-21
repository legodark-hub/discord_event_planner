import datetime
import discord
from discord import app_commands


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

        event_name = self.children[0].value
        description = self.children[1].value
        time = datetime.datetime.strptime(self.children[2].value, "%H:%M %d.%m.%Y")
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


class Event(discord.ui.View):

    def __init__(
        self,
        interaction: discord.Interaction,
        author: discord.User,
        event_name: str,
        description: str,
        time: datetime.datetime,
        participants_needed: int,
    ):
        super().__init__()
        self.interaction = interaction
        self.author = author.mention
        self.event_name = event_name
        self.description = description
        self.time = time
        self.participants_needed = int(participants_needed)
        self.participants = []
        message: discord.abc.Messageable = None

    async def is_author(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author

    async def on_timeout(self):
        # TODO: timers
        pass

    def create_message(self):
        embed = discord.Embed(
            title=self.event_name,
            description=self.description,
        )
        embed.add_field(name=f"Запросил:", value=self.author, inline=True)
        embed.add_field(
            name="Нужно участников:", value=self.participants_needed, inline=True
        )
        embed.add_field(name="Время сбора:", value=f"<t:{int(self.time.timestamp())}> \n<t:{int(self.time.timestamp())}:R>", inline=True)
        embed.add_field(
            name="Записались:",
            value="\n".join(self.participants) if self.participants else "Никого",
            inline=False,
        )
        return embed

    def participants_full(self):
        return len(self.participants) >= self.participants_needed

    async def send(self, interaction: discord.Interaction):
        embed = self.create_message()
        await interaction.response.send_message(view=self, embed=embed)
        self.message = await interaction.original_response()

    async def update_message(self):
        if self.participants_full():
            self.join.disabled = True
        else:
            self.join.disabled = False

        embed = self.create_message()
        await self.message.edit(view=self, embed=embed)

    @discord.ui.button(label="Записаться", style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.message = interaction.message

        if (
            interaction.user.mention not in self.participants
            and interaction.user.mention != self.author
        ):
            if not self.participants_full():
                await interaction.response.defer()
                self.participants.append(interaction.user.mention)
            else:
                await interaction.response.send_message(
                    "Свободных мест нет", ephemeral=True
                )
                return
        else:
            await interaction.response.send_message("Вы уже записаны", ephemeral=True)
            return

        await self.update_message()

    @discord.ui.button(label="Отписаться", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.message = interaction.message

        if interaction.user.mention == self.author:
            await interaction.response.defer()
            return
        if interaction.user.mention in self.participants:
            await interaction.response.defer()
            self.participants.remove(interaction.user.mention)
        else:
            await interaction.response.send_message("Вы не записаны", ephemeral=True)
            return

        await self.update_message()


@discord.ui.button(label="Записаться", style=discord.ButtonStyle.green)
async def join(interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.defer()


async def setup(bot):
    bot.tree.add_command(Commands(name="event", description="event commands"))
