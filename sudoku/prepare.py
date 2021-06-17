import glob
import os
import sys

import toml
from discord.ext import commands


def cogs_modules(path: str) -> list:
    return [file.replace("./", "").replace("/", ".")[:-3] for file in glob.glob(f"{path}/*.py") if
            "__init__" not in file]


def get_settings(path: str) -> dict:
    with open(path, "r") as f:
        return toml.load(f)


def cogs_list(path: str) -> list:
    cog_paths: list = cogs_modules(path)
    cogs: list
    try:
        cogs = [__import__(cog, fromlist=['*']) for cog in cog_paths]
    except ModuleNotFoundError as err:
        print(f"Error importing module:\n{err}")
        sys.exit(-1)

    return cogs


def add_cogs_to_bot(bot: commands.Bot, settings: dict, cogs: list):
    for cog in cogs:
        try:
            bot.add_cog(cog.init_class(bot, settings))
        except AttributeError:
            print("One of the imported cogs is missing `init_class(bot)`")


def env_to_settings(settings: dict):
    owner = {}
    if 'owner' in settings.keys():
        owner = settings['owner']

    owner['id'] = os.getenv("OWNER_ID")
    settings['owner'] = owner
