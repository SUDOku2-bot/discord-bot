import json
import os

import discord.ext.commands
import requests

from sudoku import logger

API_url = os.getenv("API_URL")
prefix_url = f"{API_url}servers/prefix"


def server_prefix(bot: discord.ext.commands.Bot, message: discord.Message):
    response = requests.get(prefix_url, params={"id": message.guild.id})
    if response.status_code != 200:
        res: dict = json.loads(response.text)
        logger.error(f"server_prefix | [{message.author.id}] : [{message.content}]")
        logger.error(f"{res}")

    return response.text
