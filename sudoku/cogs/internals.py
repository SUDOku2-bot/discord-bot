from discord.ext import commands


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
        if not self.is_bot_owner(str(ctx.author.id)):
            await ctx.send("This command is reserved to the bot owner")
            return


def init_class(bot: commands.Bot, settings: dict):
    return Internals(bot, settings)
