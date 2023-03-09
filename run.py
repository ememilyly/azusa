#!/usr/bin/env python
import discord
from discord.ext import commands
from lib import azusa, helpers
import logging

import asyncio
import os

discord.utils.setup_logging(level=logging.INFO)
_log = logging.getLogger(__name__)


async def main():
    async with bot:
        for ext in bot.available_exts:
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
    bot = azusa.Azusa(config["bot"]["prefix"], intents=discord.Intents.all())
    bot.owner_id = int(config["bot"]["ownerid"])

    if config["ai"]["openai_error_messages"]:
        if config["ai"]["openai_api_key"] and config["ai"]["personality_prompt"]:
            bot.personality = config["ai"]["personality_prompt"]

    bot.config = config

    asyncio.run(main())
