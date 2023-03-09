from discord.ext import commands
import logging

import requests
# import openai

_log = logging.getLogger(__name__)


class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @commands.command(
        help="Generate images through DeepAI text2img",
        hidden=True
    )
    async def text2img(
        self,
        ctx,
        *,
        prompt: str = commands.parameter(
            description="Prompt for DeepAI to generate with"
        )
    ):
        r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={"text": prompt, "grid_size": "1"},
            headers={'api-key': self.bot.config["ai"]["deepai_api_key"]}
        )
        await ctx.send(r.json()["output_url"])


async def setup(bot):
    _log.info(f"loading {__name__}")
    if bot.config["ai"]["deepai_api_key"]:
        await bot.add_cog(ai(bot))
    else:
        e = "no DeepAI api key found, not loading"
        _log.warning(e)
        raise commands.ExtensionError(e, name=__name__)
