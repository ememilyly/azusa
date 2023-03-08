#!/usr/bin/env python
import discord
from discord.ext import commands

import asyncio
import os
import logging
from configparser import ConfigParser

discord.utils.setup_logging(level=logging.INFO)
_log = logging.getLogger(__name__)

async def load_extensions():
    for f in os.listdir('cogs'):
        if f.endswith('.py'):
            cog = f[:-3]
            try:
                await bot.load_extension(f'cogs.{cog}')
            except Exception as e:
                continue

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot.config['bot']['token'])


if __name__ == '__main__':
    if os.path.isfile('bot.cfg'):
        config = ConfigParser()
        config.read('bot.cfg')
    else:
        raise OSError("bot.cfg not found")

    # TODO: intents??
    # https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.intents
    bot = commands.Bot(config['bot']['prefix'], intents=discord.Intents.all())
    bot.owner_id = int(config['bot']['ownerid'])
    bot.config = config

    asyncio.run(main())
