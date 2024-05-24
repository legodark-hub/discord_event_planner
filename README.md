# Discord Event Planner

Discord Event Planner is a bot designed to help users organize and participate in scheduled events within a Discord server. It integrates with a PostgreSQL database to store information about events and participants.

## Features

- Create and delete events
- Notify users about upcoming events
- View your history of events as author or participant

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/legodark-hub/discord_event_planner.git
    cd discord_event_planner
    ```

2. Set up a virtual environment and install dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Create a bot account in the [Discord Developer Portal](https://discord.com/developers/applications).
In the Installation page select the `bot` and `applications.commands` scope, generate Install link and open it in browser to invite the created bot to your server. In the Bot page generate the bot token.

4. Set up PostgreSQL

5. Create a `.env` file and create there variables with your discord token and connection link to your database:

    ```bash
    DISCORD_TOKEN=your_discord_bot_token
    DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
    ```

6. Run database migrations:

    ```bash
    alembic upgrade head
    ```

7. Start the bot:

    ```bash
    python main.py
    ```

## Usage

Start typing `/` in a Discord server where this bot exists to get a list of slash commands for this bot.

## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!
