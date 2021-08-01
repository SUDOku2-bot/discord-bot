import os
import sys

from discord.ext import commands

from sudoku.logger import Logger
from sudoku.prepare import get_settings, cogs_list, add_cogs_to_bot, env_to_settings
from sudoku.servers.config import server_prefix

settings_file = "./settings.toml"

token = os.getenv("BOT_TOKEN")

bot: commands.bot = commands.AutoShardedBot(command_prefix=server_prefix)

settings: dict = get_settings(settings_file)
logger = Logger(settings['paths']['logs'])

if not env_to_settings(settings):
    print("Error reading Environment variables", file=sys.stderr)
    exit(-1)

cogs: list = cogs_list(settings['paths']['cogs'])

add_cogs_to_bot(bot, settings, cogs)
