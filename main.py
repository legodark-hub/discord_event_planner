import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from bot.commands import MyCommands

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents().all()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


@tree.command(name="ping", description="ping")
async def ping(interaction):
    await interaction.response.send_message(content="pong", ephemeral=True)


@tree.command(name="hello", description="Responds with a greeting")
async def hello(interaction):
    await interaction.response.send_message(content="Секретное сообщение")


@tree.command(name="create_event", description="Создание нового события")
async def create_event(interaction: discord.Interaction):
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


@bot.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {bot.user}")


if __name__ == "__main__":
    bot.run(TOKEN)
