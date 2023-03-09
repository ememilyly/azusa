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
        help="Generate images through dezgo text2img",
    )
    async def text2img(self, ctx, *prompt):
        # Convert member/channel mentions to text
        p = []
        for word in prompt:
            mention_regex = "^<(@|#)\\d*>$"
            # e.g. <@111222333444555666>
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

        prompt = " ".join(p)
        self.log.info(f"generating image prompt: {prompt}")
        async with ctx.typing():
            image = generate_dezgo_image(prompt, self.bot.config["ai"]["dezgo_api_key"])
            await ctx.send(file=discord.File(image, filename="image.png", spoiler=True))

    @commands.command()
    async def text(self, ctx, *args):
        pass


async def setup(bot):
    _log.info(f"loading {__name__}")
    if bot.config["ai"]["dezgo_api_key"]:
        await bot.add_cog(ai(bot))
    else:
        e = "no dezgo api key found, not loading"
        _log.warning(e)
        raise commands.ExtensionError(e, name=__name__)


# Local helpers


def generate_dezgo_image(
    prompt: str, key: str, model: str = "epic_diffusion_1_1"
) -> io.BytesIO:
    url = "https://dezgo.p.rapidapi.com/text2image"
    payload = {
        "prompt": prompt,
        "guidance": 7,
        "steps": 30,
        "sampler": "euler_a",
        "upscale": 1,
        # default given by dezgo /shrug linter fuming rn
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft",
        "model": model,
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "dezgo.p.rapidapi.com",
    }
    r = requests.post(url, data=payload, headers=headers)

    return io.BytesIO(r.content)
