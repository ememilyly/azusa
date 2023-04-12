from discord.ext import commands
import logging

import requests

_log = logging.getLogger(__name__)


class gw2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @commands.command(aliases=("fotm",), help="Check daily fractals")
    async def fractals(self, ctx):
        async with ctx.typing():
            # get all dailies
            dailies = request_gw2_api("achievements/daily")
            # get fractal names from daily ids
            fractal_ids = ",".join(str(i["id"]) for i in dailies['fractals'])
            fractal_achieves = request_gw2_api(
                "achievements",
                params={"ids": fractal_ids}
            )
            fractal_names = [i["name"].lstrip("Daily Tier 4 ") for i in fractal_achieves if "Tier 4" in i["name"]]

            await ctx.reply("\n".join(fractal_names))


async def setup(bot):
    _log.info(f"loading {__name__}")
    await bot.add_cog(gw2(bot))


def request_gw2_api(endpoint: str, params: dict = {}) -> list:
    url = f"https://api.guildwars2.com/v2/{endpoint}"

    r = requests.get(url, params=params, timeout=20)
    _log.debug(r.json())
    return r.json()
