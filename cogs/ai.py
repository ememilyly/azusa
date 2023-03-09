from discord.ext import commands
import discord
from lib import helpers
import logging

_log = logging.getLogger(__name__)


class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @commands.Cog.listener()
    async def on_message(self, message):
        # don't reply to commands unless we want to
        if message.content.startswith(self.bot.command_prefix):
            if message.content.split(' ')[0] not in self.bot.commands_and_aliases:
                # await message.reply("dumbass")
                pass
        else:
            if f"<@{self.bot.user.id}>" in message.content or (
                message.type == discord.MessageType.reply
                and message.reference.cached_message.author.id == self.bot.user.id
            ):
                async with message.channel.typing():
                    await message.reply(helpers.generate_openai_chat(message.clean_content))

    @commands.command(
        aliases=("t2i",),
        help="Generate images through dezgo text2img",
    )
    async def text2img(self, ctx, *, prompt: commands.clean_content() = None):
        if prompt:
            self.log.info(f"generating image prompt: {prompt}")
            async with ctx.typing():
                try:
                    image = helpers.generate_dezgo_image(prompt)
                except Exception as e:
                    self.log.error(e)
                    await ctx.reply('```' + str(e) + '```')
                    return
                await ctx.send(
                    file=discord.File(image, filename="image.png", spoiler=True)
                )
        else:
            prompt = f"i ({ctx.author.display_name}) asked you to generate an image but you need to know what the image would be of and they didn't tell you"

            async with ctx.typing():
                await ctx.reply(helpers.generate_openai_chat(prompt))

    @commands.command()
    async def chat(self, ctx, *args):
        async with ctx.typing():
            if args:
                await ctx.send(
                    helpers.generate_openai_chat(
                        " ".join(args),
                    )
                )
            else:
                await ctx.send(helpers.generate_rude_response_missing_arg(ctx))


async def setup(bot):
    _log.info(f"loading {__name__}")
    # TODO: move this to stop loading just the command?
    if bot.config["ai"]["openai_api_key"]:
        await bot.add_cog(ai(bot))
    else:
        e = "no openai api key found, not loading"
        _log.warning(e)
        raise commands.ExtensionError(e, name=__name__)
