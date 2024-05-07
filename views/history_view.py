import math
import uuid
import discord
import database.db as db


class HistoryView(discord.ui.View):
    def __init__(self, discord_id, role):
        super().__init__(timeout=None)
        self.message: discord.abc.Messageable = None
        self.discord_id = discord_id
        self.role = role
        self.current_page = 1
        self.separator = 10
        self.data = None
        self.embed = None
        self.count: int = 0

    async def get_current_page_data(self):
        if self.role == "автор":
            self.data = await db.get_events_by_author_id(
                discord_id=self.discord_id,
                page=self.current_page,
                per_page=self.separator,
            )
        else:
            self.data = await db.get_events_by_participant_id(
                discord_id=self.discord_id,
                page=self.current_page,
                per_page=self.separator,
            )

    def create_embed(self):
        embed = discord.Embed(title=f"События, в которых вы {self.role} ({self.count})")
        for event in self.data:
            embed.add_field(
                name=f"{event.name}",
                value=f"""{event.description[0:500]}... 
                Запросил: <@{event.author_id}>, время сбора: <t:{int(event.time.timestamp())}> 
                Участники: {", ".join([f"<@{user.discord_id}>" for user in event.participants])}
                """,
                inline=False,
            )
        embed.set_footer(
            text=f"Страница {self.current_page} из {math.ceil(self.count / self.separator)}"
        )
        return embed

    async def update_message(self):
        await self.get_current_page_data()
        self.embed = self.create_embed()
        # self.update_buttons()
        await self.message.edit(embed=self.embed, view=self)

    async def send(self, interaction: discord.Interaction):
        if self.role == "автор":
            self.count = await db.get_events_by_author_id_count(
                discord_id=self.discord_id
            )
        else:
            self.count = await db.get_events_by_participant_id_count(
                discord_id=self.discord_id
            )
        await self.get_current_page_data()
        self.embed = self.create_embed()
        await interaction.response.send_message(
            embed=self.embed, view=self, ephemeral=True
        )
        self.message = await interaction.original_response()

    @discord.ui.button(
        label="|<",
        style=discord.ButtonStyle.gray,
        custom_id=str(uuid.uuid4()),
    )
    async def first_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.current_page = 1
        await self.update_message()

    @discord.ui.button(
        label="<",
        style=discord.ButtonStyle.gray,
        custom_id=str(uuid.uuid4()),
    )
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.current_page > 1:
            self.current_page -= 1
            await self.update_message()

    @discord.ui.button(
        label=">",
        style=discord.ButtonStyle.gray,
        custom_id=str(uuid.uuid4()),
    )
    async def forward(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        if self.current_page < math.ceil(self.count / self.separator):
            self.current_page += 1
            await self.update_message()

    @discord.ui.button(
        label=">|",
        style=discord.ButtonStyle.gray,
        custom_id=str(uuid.uuid4()),
    )
    async def last_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.current_page = math.ceil(self.count / self.separator)
        await self.update_message()
