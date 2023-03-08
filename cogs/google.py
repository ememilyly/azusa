from discord.ext import commands
import logging
from configparser import ConfigParser
from google_images_search import GoogleImagesSearch

_log = logging.getLogger(__name__)

class google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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
    _log.info(f'Loading {__name__}')
    if bot.config['google']['api_key'] and bot.config['google']['engine_id']:
        await bot.add_cog(google(bot))
    else:
        e = 'No google api config found, not loading'
        _log.warning(e)
        raise commands.ExtensionError(e, name=__name__)
