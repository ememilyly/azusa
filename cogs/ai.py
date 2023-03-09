from discord.ext import commands
import discord
from lib import helpers
import logging

import re
import requests
# import openai

_log = logging.getLogger(__name__)


class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @commands.command(
        aliases=("t2i",),
        help="Generate images through DeepAI text2img",
    )
    async def text2img(self, ctx, *prompt):
        # Convert embedded member/channel names to text
        p = []
        for word in prompt:
            mention_regex = '^<(@|#)\\d*>$'
            # e.g. <@141641110090022914>
            if re.match(mention_regex, word):
                obj = helpers.get_object_from_mention(ctx, word)
                if isinstance(obj, discord.Member):
                    word = obj.nick
                else:
                    word = obj.name
            p.append(word)

        prompt = ' '.join(p)
        self.log.info(f"generating image prompt: {prompt}")
        async with ctx.typing():
            r = requests.post(
                "https://api.deepai.org/api/text2img",
                data={"text": prompt, "grid_size": "1"},
                headers={'api-key': self.bot.config["ai"]["deepai_api_key"]}
            )
            self.log.info(r.json())
            if "err" in r.json():
                await ctx.send(r.json()["err"])
            elif "output_url" in r.json():
                await ctx.send(r.json()["output_url"])


async def setup(bot):
    _log.info(f"loading {__name__}")
    if bot.config["ai"]["deepai_api_key"]:
        await bot.add_cog(ai(bot))
    else:
        e = "no DeepAI api key found, not loading"
        _log.warning(e)
        raise commands.ExtensionError(e, name=__name__)
