import os

from discord.ext import commands

from sudoku.prepare import get_settings, cogs_list, add_cogs_to_bot
from sudoku.servers.config import server_prefix

settings_file = "./settings.toml"

token = os.getenv("BOT_TOKEN")

bot: commands.bot = commands.Bot(command_prefix=server_prefix)

settings: dict = get_settings(settings_file)
cogs: list = cogs_list(settings['paths']['cogs'])

add_cogs_to_bot(bot, settings, cogs)

if __name__ == "__main__":
    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("Shutting down...")
        bot.close()
        # TODO: close sockets and make sure to commit every change
