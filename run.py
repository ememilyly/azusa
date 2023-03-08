#!/usr/bin/env python
import discord
from discord.ext import commands

import asyncio
import os
import logging
from configparser import ConfigParser

async def load_extensions():
    for f in os.listdir('cogs'):
        if f.endswith('.py'):
            cog = f[:-3]
            await bot.load_extension(f'cogs.{cog}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot.config['bot']['token'])

discord.utils.setup_logging(level=logging.INFO)

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
