import asyncio
import datetime
import uuid
import discord


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
        super().__init__(timeout=None)
        self.interaction = interaction
        self.author = author
        self.event_name = event_name
        self.description = description
        self.time = time
        self.participants_needed = int(participants_needed)
        self.participants = []
        self.id = uuid.uuid4()
        self.reminder_time = 5
        embed = self.create_message()
        message: discord.abc.Messageable = None

    async def is_author(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author

    async def set_reminder(self):
        delay_minutes: datetime.timedelta
        if self.time - datetime.datetime.now() >= datetime.timedelta(
            minutes=self.reminder_time
        ):
            delay_minutes = (self.time - datetime.datetime.now()) - datetime.timedelta(
                minutes=self.reminder_time
            )
        else:
            delay_minutes = self.time - datetime.datetime.now()
        await asyncio.sleep(delay_minutes.total_seconds())
        message = self.create_reminder_message()
        await self.author.send(embed=message)
        for user in self.participants:
            await user.send(embed=message)

    def create_reminder_message(self):
        reminder_embed = discord.Embed(
            title=f"У вас запланировано событие <t:{int(self.time.timestamp())}:R>:",
            description=f"{self.event_name}",
        )
        reminder_embed.add_field(
            name=f"Описание:", value=self.description, inline=False
        )
        reminder_embed.add_field(
            name=f"Запросил:", value=self.author.mention, inline=False
        )
        reminder_embed.add_field(
            name="Записались:",
            value=(
                "\n".join([user.mention for user in self.participants])
                if self.participants
                else "Никого"
            ),
            inline=False,
        )
        return reminder_embed

    def create_message(self):
        embed = discord.Embed(
            title=self.event_name,
            description=self.description,
        )
        embed.add_field(name=f"Запросил:", value=self.author.mention, inline=True)
        embed.add_field(
            name="Нужно участников:", value=self.participants_needed, inline=True
        )
        embed.add_field(
            name="Время сбора:",
            value=f"<t:{int(self.time.timestamp())}> \n<t:{int(self.time.timestamp())}:R>",
            inline=True,
        )
        embed.add_field(
            name="Записались:",
            value=(
                "\n".join([user.mention for user in self.participants])
                if self.participants
                else "Никого"
            ),
            inline=False,
        )
        return embed

    def participants_full(self):
        return len(self.participants) >= self.participants_needed

    async def send(self, interaction: discord.Interaction):
        self.embed = self.create_message()
        await interaction.response.send_message(view=self, embed=self.embed)
        self.message = await interaction.original_response()
        await self.set_reminder()

    async def update_message(self):
        if self.participants_full():
            self.join.disabled = True
        else:
            self.join.disabled = False

        if not self.participants:
            self.decline.disabled = True
        else:
            self.decline.disabled = False

        self.embed = self.create_message()
        await self.message.edit(view=self, embed=self.embed)

    @discord.ui.button(
        label="Записаться", style=discord.ButtonStyle.green, custom_id=str(uuid.uuid4())
    )
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.message = interaction.message

        if (
            interaction.user
            not in self.participants
            # # TODO: для тестов, раскомментировать
            # and interaction.user != self.author
        ):
            if not self.participants_full():
                await interaction.response.defer()
                self.participants.append(interaction.user)
            else:
                await interaction.response.send_message(
                    "Свободных мест нет", ephemeral=True
                )
                return
        else:
            await interaction.response.send_message("Вы уже записаны", ephemeral=True)
            return
        await self.update_message()

    @discord.ui.button(
        label="Отписаться",
        style=discord.ButtonStyle.red,
        custom_id=str(uuid.uuid4()),
        disabled=True,
    )
    async def decline(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.message = interaction.message

        if interaction.user == self.author:
            await interaction.response.defer()
            return
        if interaction.user in self.participants:
            await interaction.response.defer()
            self.participants.remove(interaction.user)
        else:
            await interaction.response.send_message("Вы не записаны", ephemeral=True)
            return

        await self.update_message()
