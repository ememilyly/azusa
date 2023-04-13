from discord.ext import commands
import logging

import requests

_log = logging.getLogger(__name__)

# There's no way to retrieve these through the API so must hardcode :(
# https://wiki.guildwars2.com/wiki/Fractals_of_the_Mists#Daily_Fractals
# scrape from wiki?
# key is the t1 rec as they're always unique and this makes it a lot cleaner
DAILY_RECS_TABLE = {
    2: {2: "Uncategorized", 37: "Siren's Reef", 53: "Underground Facility"},
    6: {6: "Cliffside", 28: "Volcanic", 61: "Aquatic Ruins"},
    10: {10: "Molten Boss", 32: "Swampland", 65: "Aetherblade"},
    14: {14: "Aetherblade", 34: "Thaumanova Reactor", 53: "Sunqua Peak"},
    19: {19: "Volcanic", 37: "Siren's Reef", 66: "Urban Battleground"},
    15: {15: "Thaumanova Reactor", 41: "Twilight Oasis", 60: "Solid Ocean"},
    24: {24: "Shattered Observatory", 35: "Solid Ocean", 75: "Sunqua Peak"},
    25: {25: "Sunqua Peak", 36: "Uncategorized", 69: "Cliffside"},
    12: {12: "Siren's Reef", 40: "Molten Boss", 67: "Deepstone"},
    8: {8: "Underground Facility", 31: "Urban Battleground", 54: "Siren's Reef"},
    11: {11: "Deepstone", 39: "Molten Furnace", 59: "Twilight Oasis"},
    18: {18: "Captain Mai Trin Boss", 27: "Snowblind", 64: "Thaumanova Reactor"},
    4: {4: "Urban Battleground", 30: "Chaos", 58: "Molten Furnace"},
    16: {16: "Twilight Oasis", 42: "Captain Mai Trin Boss", 62: "Uncategorized"},
    5: {5: "Swampland", 48: "Nightmare", 68: "Snowblind"},
}


class gw2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @commands.command(aliases=("fotm",), help="Check daily fractals")
    async def fractals(self, ctx, tomorrow: str = None):
        endpoint = "daily/tomorrow" if tomorrow == "tomorrow" else "daily"
        message = ["Daily tiered:"]
        async with ctx.typing():
            # get all dailies
            dailies = request_gw2_api(f"achievements/{endpoint}")
            # get fractal names from daily ids
            fractal_ids = ",".join(str(i["id"]) for i in dailies["fractals"])
            fractal_achieves = request_gw2_api(
                "achievements", params={"ids": fractal_ids}
            )
            message += [
                # "Daily Tier X Fractal" -> "Fractal"
                i["name"][13:] for i in fractal_achieves if "Tier 4" in i["name"]
            ]
            # look up recs
            message.append("\nDaily recs:")
            rec_scales = [
                # "Daily Recommended Fractal-Scale XX" -> XX
                int(i["name"].split()[-1]) for i in fractal_achieves if "Recommended" in i["name"]
            ]
            t1_rec = sorted(rec_scales)[0]
            daily_recs = DAILY_RECS_TABLE[t1_rec]
            for scale, name in daily_recs.items():
                message.append(f"{name} (rec {scale})")

            await ctx.reply("\n".join(message))


async def setup(bot):
    _log.info(f"loading {__name__}")
    await bot.add_cog(gw2(bot))


def request_gw2_api(endpoint: str, params: dict = {}) -> list:
    url = f"https://api.guildwars2.com/v2/{endpoint}"

    r = requests.get(url, params=params, timeout=20)
    _log.debug(r.json())
    return r.json()
