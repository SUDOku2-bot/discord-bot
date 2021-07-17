import json

import discord
from discord.ext import commands

from sudoku.api_utils import patch_request, error_chk


class Leveling(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: dict):
        self.bot = bot
        self.settings = settings

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        api_url = self.settings['API_URL'] + "levels/xp"
        response = patch_request(api_url, data={
            "server_id": str(message.guild.id),
            "user_id": str(message.author.id)
        })

        res: dict = json.loads(response.text)

        if error_chk(res):
            with open(self.settings['paths']['logs'], 'a+') as f:
                f.write(f"[ERROR] leveling.on_message | [{message.author.id}] : [{message.content}]")

        if "trigger" not in res.keys():
            return

        if not res['trigger']:
            return

        await message.channel.send(f"<@{message.author.id}> is now level {res['level']}")
        # TODO: Check if user needs to get a role

    @commands.command(aliases=['lvltoggle', 'levelstoggle', 'leveling'])
    async def toggle_leveling(self, ctx: commands.Context):
        # TODO: Check user's permissions lmao
        api_url = self.settings['API_URL']
        response = patch_request(f"{api_url}servers", data={
            "leveling": 1,
            "server_id": str(ctx.guild.id)
        })

        res: dict = json.loads(response.text)

        if error_chk(res):
            await ctx.send(f"Error!\n```\n{res['content']}\n```")

        await ctx.send(f"Leveling {'enabled' if res['content'] else 'disabled'}")


def init_class(bot: commands.Bot, settings: dict):
    return Leveling(bot, settings)
