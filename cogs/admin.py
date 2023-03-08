from discord.ext import commands
import logging
from configparser import ConfigParser
import subprocess
import os

_log = logging.getLogger(__name__)

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('cogs',))
    @commands.is_owner()
    async def listcogs(self, ctx):
        loaded_cogs = self.bot.cogs.keys()
        unloaded_cogs = []
        for cog in available_cogs():
            if cog not in loaded_cogs:
                unloaded_cogs.append(cog)

        message = 'Loaded cogs:\n`' + \
            '`, `'.join(sorted(loaded_cogs)) + '`'
        if unloaded_cogs:
            message += '\n\nUnloaded cogs:\n`' + \
                '`, `'.join(sorted(unloaded_cogs)) + '`'

        await ctx.send(message)

    @commands.command(aliases=('load',))
    @commands.is_owner()
    async def loadcog(self, ctx, *args):
        if not args:
            await ctx.send('Please specify which cogs to load.')
        else:
            _available_cogs = available_cogs()
            for cog in args:
                if cog not in _available_cogs:
                    await ctx.send(f'Can\'t find `{cog}` :frowning:')
                elif cog in self.bot.cogs.keys():
                    await ctx.send(f'`{cog}` is already loaded.')
                else:
                    try:
                        await self.bot.load_extension(f'cogs.{cog}')
                    except Exception as e:
                        await ctx.send(f'Failed to load {cog} :sob:\n```{e}```')
                    else:
                        await ctx.send(f'Loaded `{cog}` :muscle:')

    @commands.command(aliases=('unload',))
    @commands.is_owner()
    async def unloadcog(self, ctx, *args):
        if not args:
            await ctx.send('Please specify which cogs to unload.')
        else:
            _loaded_cogs = self.bot.cogs.keys()
            for cog in args:
                if cog not in _loaded_cogs:
                    await ctx.send(f'Unknown cog `{cog}` :frowning:')
                else:
                    await self.bot.unload_extension(f'cogs.{cog}')
                    await ctx.send(f'Unloaded `{cog}` :wave:')

    @commands.command(aliases=('reload',))
    @commands.is_owner()
    async def reloadcog(self, ctx, *args):
        if not args:
            cogs = sorted(self.bot.cogs.keys())
            for cog in cogs:
                await self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(f'{len(self.bot.cogs)} cogs reloaded: `{"`, `".join(cogs)}`')
            self.bot.config = reload_cfg('bot.cfg')
            self.bot.command_prefix = self.bot.config['bot']['prefix']
            await ctx.send('Reloaded config :muscle:')
        else:
            for cog in args:
                if cog in ('cfg', 'config'):
                    self.bot.config = reload_cfg('bot.cfg')
                    self.bot.command_prefix = self.bot.config['bot']['prefix']
                    await ctx.send('Reloaded config :slight_smile:')
                elif cog in self.bot.cogs.keys():
                    await self.bot.reload_extension(f'cogs.{cog.lower()}')
                    await ctx.send(f'Reloaded `{cog}` :muscle:')
                else:
                    await ctx.send(f'Unknown cog `{cog}` :frowning:')

    @commands.command()
    @commands.is_owner()
    async def git(self, ctx, *args):
        if len(args) == 1:
            if args[0] == 'pull':
                res = subprocess.check_output(['git', 'pull']).decode('utf-8')
                await ctx.send('```' + res + '```')
            elif args[0] == 'status':
                subprocess.run(['git', 'remote', 'update'])
                res = subprocess.check_output(['git', 'status']).decode('utf-8')
                await ctx.send('```' + res + '```')

async def setup(bot):
    await bot.add_cog(admin(bot))

# Helpers

def reload_cfg(path):
    config = ConfigParser()
    config.read(path)
    return config

def available_cogs():
    cogs = []
    for cog in os.listdir('cogs'):
        if cog.endswith('.py'):
            cogs.append(cog[:-3])

    return cogs
