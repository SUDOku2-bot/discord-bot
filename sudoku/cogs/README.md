# Cogs

This file will explain how to make SUDOku2 compatible COGS. It's reather easy but it's worth giving you a template so
everyone can make their own.

## Why a template

It uses a particular way to load and unload them at runtime that makes use of a particular function to initialize the
class correctly.

## Template

```python
from discord.ext import commands


class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['test'])
    async def my_command(self, ctx: commands.Context):
        await ctx.send("Pong! Poggers!")


def init_class(bot: commands.Bot, settings: dict):
    return MyCog(bot)
```

## Limits

As long as a Cog can do it, then your own cog can implement it!
