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
        message: discord.abc.Messageable = None

    async def is_author(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author

    async def on_timeout(self):
        # TODO: timer for event notification for participants
        pass

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

    @discord.ui.button(
        label="Записаться", style=discord.ButtonStyle.green, custom_id="join"
    )
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.message = interaction.message

        if (
            interaction.user not in self.participants
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
        label="Отписаться", style=discord.ButtonStyle.red, custom_id="cancel"
    )
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
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
