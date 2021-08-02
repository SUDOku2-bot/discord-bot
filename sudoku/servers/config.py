import json
import os
from functools import lru_cache

import discord.ext.commands
import requests

from sudoku import logger

API_url = os.getenv("API_URL")
prefix_url = f"{API_url}servers/prefix"


def server_prefix(bot: discord.ext.commands.Bot, message: discord.Message):
    prefix: str = get_prefix(message.guild.id)
    if prefix is None:
        logger.error(f"server_prefix | [{message.author.id}] : [{message.content}]")
        return "su!"
    return prefix


@lru_cache(maxsize=128)
def get_prefix(server_id: int):
    response = requests.get(prefix_url, params={"id": server_id})
    if response.status_code != 200:
        res: dict = json.loads(response.text)
        logger.error(f"{res}")
        return None

    return response.text
