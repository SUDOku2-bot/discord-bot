import json

import discord
import requests
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import has_permissions

from sudoku.api_utils import patch_request, error_chk
from sudoku import logger, server_prefix


class Leveling(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: dict):
        self.bot = bot
        self.settings = settings

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith(server_prefix(self.bot, message)):
            return

        api_url = self.settings['API_URL'] + "levels/xp"
        response = patch_request(api_url, data={
            "server_id": str(message.guild.id),
            "user_id": str(message.author.id)
        })

        res: dict = json.loads(response.text)

        if error_chk(res):
            logger.error(f"leveling.on_message | [{message.author.id}] : [{message.content}]")

        if "trigger" not in res.keys():
            return

        if not res['trigger']:
            return

        # Level up happened
        await self.on_level_up(message, res['level'])

        await message.channel.send(f"<@{message.author.id}> is now level {res['level']}")

    async def on_level_up(self, message: discord.Message, level: int):
        response = requests.get(f"{self.settings['API_URL']}levels/role", params={
            "server_id": message.guild.id,
            "level": level
        })

        json_body = response.json()
        if json_body is None or json_body['status'] != "ok":
            return

        json_body['content']: list
        if len(json_body['content']) < 1:
            return

        author: discord.Member = message.author
        for role_id in json_body['content']:
            try:
                role = get(message.guild.roles, id=int(role_id))
                await author.add_roles(role, reason="Level up")
            except discord.errors.Forbidden as e:
                await message.channel.send(f"Error: {e}")
                return

    @commands.command(aliases=['lvltoggle', 'levelstoggle', 'leveling'])
    @has_permissions(administrator=True)
    async def toggle_leveling(self, ctx: commands.Context):
        print("AAAAAAAAAAAAAAAAA")
        api_url = self.settings['API_URL']
        response = patch_request(f"{api_url}servers", data={
            "leveling": 1,
            "server_id": str(ctx.guild.id)
        })

        res: dict = json.loads(response.text)

        if error_chk(res):
            await ctx.send(f"Error!\n```\n{res['content']}\n```")

        await ctx.send(f"Leveling {'enabled' if res['content'] else 'disabled'}")

    @commands.command(aliases=['roleup', 'levels_role', 'levelrole', 'levelsrole'])
    @has_permissions(ban_members=True)
    async def level_role(self, ctx: commands.Context, mode: str = None, role: discord.Role = None, level: int = None):
        if mode is None:
            await ctx.send(f"Usage: `{ctx.message.content} <add/remove/list> <role_id> <level>`")
            return

        if mode == "add":
            if level is None or role is None:
                await ctx.send("Usage: add <role_id> <level>")
                return

            body = {
                "server_id": str(ctx.guild.id),
                "role_id": str(role.id),
                "level": level
            }

            headers = {
                "content-type": "application/json"
            }

            response = requests.post(f"{self.settings['API_URL']}levels/role", data=json.dumps(body), headers=headers)
            res_json = response.json()

            if "status" not in res_json.keys() or res_json["status"] != "ok":
                await ctx.send(f"Error while executing the command: {res_json['error']}")
                return

            await ctx.send(f"Set Automatic Role setup for role: `{role}` at level `{level}`")
        elif mode == "remove":
            if role is None:
                await ctx.send("Usage: remove <role_id>")
                return

            body = {
                "server_id": str(ctx.guild.id),
                "role_id": str(role.id),
            }

            headers = {
                "content-type": "application/json"
            }

            response = requests.delete(f"{self.settings['API_URL']}levels/role", data=json.dumps(body), headers=headers)
            res_json = response.json()

            if error_chk(res_json):
                await ctx.send(f"Error while executing the command: {res_json['error']}")
                return

            await ctx.send(f"Automatic Role removed for role: `{role}`")
        elif mode == "list":
            params = {
                "server_id": str(ctx.guild.id)
            }

            response = requests.get(f"{self.settings['API_URL']}levels/role", params=params)
            res_json = response.json()

            if error_chk(res_json):
                await ctx.reply(f"Error while executing the command: {res_json['error']}")
                return

            message: str = ""
            for role_id in res_json['content']:
                role: discord.Role = get(ctx.guild.roles, id=int(role_id[0]))
                message += f"`{role.name}` => lvl `{role_id[1]}`\n"

            await ctx.reply(message if len(message) > 1 else "No roles found")


def init_class(bot: commands.Bot, settings: dict):
    return Leveling(bot, settings)
