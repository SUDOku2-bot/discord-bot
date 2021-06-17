from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        print(f"Successfully Connected as {self.bot.user.display_name}")


def init_class(bot: commands.Bot):
    return Greetings(bot)
