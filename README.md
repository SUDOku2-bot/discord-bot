# Discord Bot

The Discord bot part of SUDOku 2

- [Cogs](#cogs)

## Configuration

The following Environment variables are given:

- `BOT_TOKEN`: Bot token from https://discord.com/developers/applications/_YOUR_APP_ID_/bot
- `OWNER_ID`: The bot owner ID, used for cogs loading/unloading and critical commands
- `API_URL`: URL of the SUDOku2 API. Example: `https://localhost:5000/api/v1/`

## Run it

Start `main.py`. In the future this will be a Docker container

---

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
