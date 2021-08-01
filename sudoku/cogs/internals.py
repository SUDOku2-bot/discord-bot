import re

import discord
from discord.ext import commands

from sudoku import server_prefix


class Internals(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: dict):
        self.bot = bot
        self.settings = settings

    def is_bot_owner(self, author_id: str):
        if "owner" not in self.settings or "id" not in self.settings["owner"]:
            return False
        return author_id == self.settings["owner"]["id"]

    @commands.Cog.listener()
    async def on_connect(self):
        print(f"Successfully Connected as {self.bot.user.display_name}")

    @commands.command(aliases=['remove_cog', 'rmcog'])
    async def unload_cog(self, ctx: commands.Context, cog_name: str):
        if not self.is_bot_owner(str(ctx.author.id)):
            await ctx.send("Very funny! WOW\nChat please laugh at this epic fail")
            return

        if cog_name not in self.bot.cogs.keys():
            await ctx.send(f"Cog `{cog_name}` is NOT loaded")
            return

        if cog_name == self.__class__.__name__:
            await ctx.send(f"Cog `{cog_name}` cannot be unloaded")
            return

        self.bot.remove_cog(cog_name)
        await ctx.send(f"Cog `{cog_name}` has been removed")

    @commands.command(aliases=['cogs', 'lscogs', 'lscog'])
    async def list_cogs(self, ctx: commands.Context):
        if not self.is_bot_owner(str(ctx.author.id)):
            await ctx.send("This command is reserved to the bot owner")
            return

        message: str = "Currently loaded cogs:\n"
        for cog in self.bot.cogs.keys():
            message += f"`{cog}`\n"

        await ctx.send(message)

    @commands.command(aliases=['addcog', 'add_cog', 'mkcog'])
    async def load_cog(self, ctx: commands.Context, cog_name: str):
        """Opens the file named {cog_name}.py and executes the init_class() function in it.
        Adds the corresponding cog Class to the loaded Cogs
        """

        if not self.is_bot_owner(str(ctx.author.id)):
            await ctx.send("This command is reserved to the bot owner")
            return

        if cog_name in self.bot.cogs:
            await ctx.send(f"Cog `{cog_name}` already loaded")
            return

        if cog_name == self.__class__.__name__:
            await ctx.send(f"Cog `{cog_name}` cannot be loaded")
            return

        cog_name = cog_name.lower()

        module_path: str = self.settings['paths']['cogs'].replace('./', '').replace('//', '/')
        if module_path[-1] == '/':
            module_path = module_path[:-1]
        module_name = f"{module_path.replace('/', '.')}.{cog_name}"

        try:
            module = __import__(module_name, fromlist=['*'])
        except ModuleNotFoundError as err:
            await ctx.send(f"Failed to import {module_name}\n{err}")
            return

        if module is None:
            await ctx.send(f"Failed to import {cog_name}")
            return

        self.bot.add_cog(module.init_class(self.bot, self.settings))
        await ctx.send(f"Cog {cog_name} successfully loaded")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.user.mentioned_in(message):
            await message.reply(f"Hello, your server's prefix is: `{server_prefix(self.bot, message)}`")


def init_class(bot: commands.Bot, settings: dict):
    return Internals(bot, settings)
