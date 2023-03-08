from discord.ext import commands
import logging
from configparser import ConfigParser
from udpy import UrbanClient
from google_images_search import GoogleImagesSearch

_log = logging.getLogger(__name__)

class stuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('ud',))
    async def urbandict(self, ctx, *args):
        if args:
            word = ' '.join(args)
            client = UrbanClient()
            defs = client.get_definition(word)
            if defs:
                m = defs[0].definition + '\ne.g.: ' + defs[0].example
                await ctx.send(m.replace('[','').replace(']',''))
            else:
                await ctx.send(f'No definition found for {word}')

    @commands.command(aliases=('img',))
    async def image(self, ctx, *args):
        if args:
            search = {
                'q': ' '.join(args),
                'num': 1,
                'safe': 'off',
                }

            if self.bot.config['google']['api_key'] and self.bot.config['google']['engine_id']:
                key = self.bot.config['google']['api_key']
                cx = self.bot.config['google']['engine_id']
            else:
                return

            gis = GoogleImagesSearch(key, cx)
            gis.search(search_params=search)
            await ctx.send(gis.results()[0]._url)

async def setup(bot):
    if bot.config['google']['api_key'] and bot.config['google']['engine_id']:
        await bot.add_cog(stuff(bot))
    else:
        _log.warning('No google api config found, not loading')
