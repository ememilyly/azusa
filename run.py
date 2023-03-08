#!/usr/bin/env python
import discord
from discord.ext import commands
import logging
from lib import helpers

import asyncio
import os

discord.utils.setup_logging(level=logging.INFO)
_log = logging.getLogger(__name__)


async def main():
    async with bot:
        for ext in helpers.available_exts():
            try:
                await bot.load_extension(f"cogs.{ext}")
            except commands.ExtensionError:
                continue

        await bot.start(bot.config["bot"]["token"])


if __name__ == "__main__":
    if os.path.isfile("bot.cfg"):
        config = helpers.reload_cfg("bot.cfg")
    else:
        raise OSError("bot.cfg not found")

    # TODO: intents??
    # https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.intents
    bot = commands.Bot(config["bot"]["prefix"], intents=discord.Intents.all())
    bot.owner_id = int(config["bot"]["ownerid"])
    bot.config = config

    asyncio.run(main())
