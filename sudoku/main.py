import os
import sys

import toml as toml
from discord.ext import commands

from sudoku.prepare import cogs_modules
from sudoku.servers.config import server_prefix

cogs_folder = "./cogs"
settings_file = "./settings.toml"

token = os.getenv("BOT_TOKEN")

bot: commands.bot = commands.Bot(command_prefix=server_prefix)

cog_paths: list = cogs_modules(cogs_folder)
cogs: list
try:
    cogs = [__import__(cog, fromlist=['*']) for cog in cog_paths]
except ModuleNotFoundError as err:
    print(f"Error importing module:\n{err}")
    sys.exit(-1)

settings: dict
with open(settings_file, "r") as f:
    settings = toml.load(f)

for cog in cogs:
    try:
        bot.add_cog(cog.init_class(bot, settings))
    except AttributeError:
        print("One of the imported cogs is missing `init_class(bot)`")

if __name__ == "__main__":
    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("Shutting down...")
        bot.close()
        # TODO: close sockets and make sure to commit every change
