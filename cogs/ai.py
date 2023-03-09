from discord.ext import commands
import discord
from lib import helpers
import logging

import re
import requests
import io
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
                    if obj.nick:
                        word = obj.nick
                    else:
                        word = obj.name
                else:
                    word = obj.name
            p.append(word)

        prompt = ' '.join(p)
        self.log.info(f"generating image prompt: {prompt}")

        # dezgo
        url = "https://dezgo.p.rapidapi.com/text2image"
        payload = {
            "prompt": prompt,
            "guidance": 7,
            "steps": 30,
            "sampler": "euler_a",
            "upscale": 1,
            "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft",
            "model": "epic_diffusion_1_1"
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": self.bot.config["ai"]["dezgo_api_key"],
            "X-RapidAPI-Host": "dezgo.p.rapidapi.com"
        }

        async with ctx.typing():
            r = requests.post(
                url,
                data=payload,
                headers=headers
            )

            await ctx.send(
                file=discord.File(
                    io.BytesIO(r.content),
                    filename="image.png"
                )
            )


async def setup(bot):
    _log.info(f"loading {__name__}")
    if bot.config["ai"]["deepai_api_key"]:
        await bot.add_cog(ai(bot))
    else:
        e = "no DeepAI api key found, not loading"
        _log.warning(e)
        raise commands.ExtensionError(e, name=__name__)
