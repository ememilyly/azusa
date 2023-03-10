from discord.ext import commands
from lib import helpers
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
        cmds = [cmd.name for cmd in self.bot.commands]
        prompt = f"'{ctx.author.display_name}' asked for help with what you do. let them know all the commands you support and to use `,help command` for more specific information on each one. the list of commands you know is: `{'`, `'.join(cmds)}`"
        async with ctx.typing():
            await ctx.reply(helpers.generate_openai_chat(prompt))

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
