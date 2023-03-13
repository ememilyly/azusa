from discord.ext import commands
import logging

import datetime
import ffxivweather

_log = logging.getLogger(__name__)


class ffxiv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @commands.command(help="cassie time??", hidden=True)
    async def cassie(self, ctx):
        # time = datetime.datetime.now().timestamp()
        # time = (datetime.datetime.now() + datetime.timedelta(minutes=30)).timestamp()
        # await ctx.send(datetime.datetime.fromtimestamp(time))

        zone = "Eureka Pagos"
        # https://github.com/karashiiro/ffxivweather-py
        forecast = ffxivweather.forecaster.get_forecast(place_name=zone, count=5)

        for i in forecast:
            await ctx.reply(f'{i[1]}: {i[0]["name_en"]}')


async def setup(bot):
    _log.info(f"loading {__name__}")
    await bot.add_cog(ffxiv(bot))
