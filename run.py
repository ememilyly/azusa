#!/usr/bin/env python
import discord
from discord.ext import commands
from lib import persephone, helpers, methods
import logging

import asyncio
import os

discord.utils.setup_logging(level=logging.INFO)
_log = logging.getLogger(__name__)


# add my methods
commands.Context.paged_reply = methods.paged_reply


async def main():
    async with bot:
        for ext in bot.available_extensions:
            try:
                await bot.load_extension(ext)
            except commands.ExtensionError:
                raise
                continue

        await bot.start(bot.config["bot"]["token"])


if __name__ == "__main__":
    if os.path.isfile("bot.cfg"):
        config = helpers.reload_cfg("bot.cfg")
    else:
        raise OSError("bot.cfg not found")

    bot = persephone.Persephone(config["bot"]["prefix"], intents=discord.Intents.all())
    bot.owner_id = int(config["bot"]["ownerid"])
    bot.cogs_dir = "cogs"

    # TODO: personality in config? this isn't really used yet as the prompt is
    # taken in a helper so haven't figured out giving it access to that yet
    if config["ai"]["openai_error_messages"]:
        if config["ai"]["openai_api_key"] and config["ai"]["personality_prompt"]:
            bot.personality = config["ai"]["personality_prompt"]

    bot.config = config

    asyncio.run(main())
