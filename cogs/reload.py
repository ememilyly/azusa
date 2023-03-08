from discord.ext import commands
from configparser import ConfigParser
import subprocess

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: this doesn't work anymore lol rip
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *args):
        if not args:
            for cog in self.bot.cogs.keys():
                self.bot.reload_extension(f'cogs.{cog.lower()}')
            await ctx.send(f'{len(self.bot.cogs)} cogs reloaded.')
            self.bot.config = reload_cfg('bot.cfg')
            self.bot.command_prefix = self.bot.config['bot']['prefix']
        elif len(args) == 1:
            cog = args[0].lower()
            if cog == "cfg":
                self.bot.config = reload_cfg('bot.cfg')
                self.bot.command_prefix = self.bot.config['bot']['prefix']
                await ctx.send('Config reloaded')
            elif cog in self.bot.cogs.keys():
                await ctx.send(f'Reloading {cog}...')
                self.bot.reload_extension(f'cogs.{cog.lower()}')
            else:
                await ctx.send(f'{cog} not recognised.')

        else:
            await ctx.send('Unrecognised arguments, please specify a cog.')
    
    @commands.command()
    @commands.is_owner()
    async def listcogs(self, ctx):
        await ctx.send(', '.join(self.bot.cogs.keys()).lower())

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
    await bot.add_cog(Reload(bot))

# Helpers

def reload_cfg(path):
    config = ConfigParser()
    config.read(path)
    return config
