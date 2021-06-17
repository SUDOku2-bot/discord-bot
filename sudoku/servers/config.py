import discord.ext.commands


def server_prefix(bot: discord.ext.commands.Bot, message: discord.Message):
    # TODO: Ask the database which prefix this server is using
    return "?"
