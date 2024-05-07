import asyncio
import datetime
import uuid
import discord
import database.db as db


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
        self.reminder_task = asyncio.create_task(self.set_reminder())
        self.deletion_task = asyncio.create_task(self.message_deletion())
        embed: discord.Embed = self.create_message()
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
        message = self.embed.copy()
        message.title = (
            f"У вас запланировано событие: \n{self.event_name}({self.message.jump_url})"
        )
        await self.notify_participants(embed=message)

    async def message_deletion(self):
        delay = self.time - datetime.datetime.now()
        await asyncio.sleep(delay.total_seconds())
        await self.message.edit(view=None, embed=self.embed)
        await self.message.delete(delay=60 * 10)

    async def notify_participants(self, text=None, embed=None):
        await self.author.send(content=text, embed=embed)
        for user in self.participants:
            await user.send(content=text, embed=embed)

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

    async def send(self):
        self.embed = self.create_message()
        await self.interaction.response.send_message("Событие создано", ephemeral=True)
        self.message = await self.interaction.channel.send(view=self, embed=self.embed)

        author = await db.get_user_by_id(self.author.id)
        if author is None:
            await db.add_user(self.author.id)
        await db.add_event(
            self.message.id,
            self.event_name,
            self.description,
            self.author.id,
            self.time,
            self.participants_needed,
        )

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

    def disable_buttons(self):
        self.join.disabled = True
        self.decline.disabled = True
        self.cancel.disabled = True

    @discord.ui.button(
        label="Записаться", style=discord.ButtonStyle.green, custom_id=str(uuid.uuid4())
    )
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.message = interaction.message

        if (
            interaction.user not in self.participants
            and interaction.user != self.author
        ):
            if not self.participants_full():
                await interaction.response.defer()
                self.participants.append(interaction.user)

                participant = await db.get_user_by_id(interaction.user.id)
                if participant is None:
                    await db.add_user(interaction.user.id)
                await db.add_participant(interaction.user.id, self.message.id)
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
            await db.remove_participant(interaction.user.id, self.message.id)

        else:
            await interaction.response.send_message("Вы не записаны", ephemeral=True)
            return

        await self.update_message()

    @discord.ui.button(
        label="Отменить",
        style=discord.ButtonStyle.blurple,
        custom_id=str(uuid.uuid4()),
    )
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (
            interaction.user == self.author
            or interaction.user.guild_permissions.administrator
        ):
            await interaction.response.defer()
            embed = self.embed.copy()
            embed.title = (
                f"Событие отменено автором: \n{self.event_name}"
                if not interaction.user.guild_permissions.administrator
                else f"Событие отменено админом сервера: \n{self.event_name}"
            )
            await self.notify_participants(embed=embed)
            self.reminder_task.cancel()
            self.deletion_task.cancel()
            await self.message.delete()
            self.stop()
            await db.remove_event(self.message.id)
        else:
            await interaction.response.send_message(
                "Эта команда доступна только автору события или админу сервера",
                ephemeral=True,
            )
