from discord.ext import commands
import logging

from udpy import UrbanClient

_log = logging.getLogger(__name__)


class stuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @commands.is_owner()
    @commands.command(
        help="test command",
        hidden=True,
    )
    async def test(
        self,
        ctx,
        *,
        testarg: str = commands.parameter(default="uwu", description="test command"),
    ):
        pass

    @commands.command(
        aliases=("ud",),
        help="Look up something on Urban Dictionary"
    )
    async def urbandict(
        self,
        ctx,
        *,
        term: str = commands.parameter(
            description="What you want to look up"
        )
    ):
        if term:
            client = UrbanClient()
            defs = client.get_definition(term)
            if defs:
                m = defs[0].definition + "\n```" + defs[0].example + "```"
                await ctx.reply(m.replace("[", "").replace("]", ""))
            else:
                await ctx.reply(f"No definition found for {term}")


async def setup(bot):
    _log.info(f"loading {__name__}")
    await bot.add_cog(stuff(bot))
