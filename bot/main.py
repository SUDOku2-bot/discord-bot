import os
from discord.ext import commands

from bot.servers.config import server_prefix

token = os.getenv("BOT_TOKEN")
bot: commands.bot = commands.Bot(command_prefix=server_prefix)

if __name__ == "__main__":
    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("Shutting down...")
        bot.close()
        # TODO: close sockets and make sure to commit every change
