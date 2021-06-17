from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['test'])
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong! Poggers!")


def init_class(bot: commands.Bot, settings: dict):
    return Ping(bot)
