from discord.ext import commands
import discord
from lib import helpers
import logging

_log = logging.getLogger(__name__)


class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log
        self.t2i_history = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        # don't reply to commands unless we want to
        if message.content.startswith(self.bot.command_prefix):
            cmd = message.content.split(" ")[0][1:]
            if cmd not in self.bot.commands_and_aliases:
                prompt = f"'{message.author.display_name}' tried to run a command `{self.bot.command_prefix}{cmd}` that you don't recognise. tell them you don't recognise it, and to use `{self.bot.command_prefix}help` if they need to."
                async with message.channel.typing():
                    await message.reply(helpers.generate_openai_chat(prompt))
        else:
            if f"<@{self.bot.user.id}>" in message.content:
                async with message.channel.typing():
                    await message.reply(helpers.generate_openai_chat(message.clean_content))
            elif message.type == discord.MessageType.reply:
                # TODO: follow message reference even if not cached?
                # this does work for an ok age check and snarky response tho
                # prompt = f"'{message.author.display_name}' replied to you but the message they replied to was from so long ago you forgot what it was"
                if message.reference.cached_message:
                    if message.reference.cached_message.author.id == self.bot.user.id:
                        async with message.channel.typing():
                            await message.reply(
                                helpers.generate_openai_chat(message.clean_content)
                            )

    @commands.command(
        aliases=("t2i",),
        help="Generate images through dezgo text2img",
    )
    async def text2img(self, ctx, *, prompt: commands.clean_content() = None):
        if prompt:
            if prompt == "!!":
                # Repeat last prompt
                if ctx.channel in self.t2i_history:
                    prompt = self.t2i_history[ctx.channel]
                else:
                    prompt = f"'{ctx.author.display_name}' asked you to generate an image using the last prompt but you don't remember what that prompt was"
                    async with ctx.typing():
                        await ctx.reply(helpers.generate_openai_chat(prompt))
                        return

            self.log.info(f"generating image prompt: {prompt}")
            self.t2i_history[ctx.channel] = prompt
            async with ctx.typing():
                try:
                    image = helpers.generate_dezgo_image(prompt)
                except Exception as e:
                    self.log.error(e)
                    await ctx.reply("```" + str(e) + "```")
                    return
                await ctx.send(
                    file=discord.File(
                        image,
                        filename="image.png",
                        spoiler=True
                    )
                )
        else:
            prompt = f"i ({ctx.author.display_name}) asked you to generate an image but you need to know what the image would be of and i didn't tell you"

            async with ctx.typing():
                await ctx.reply(helpers.generate_openai_chat(prompt))

    @commands.command()
    async def chat(self, ctx, *args):
        async with ctx.typing():
            if args:
                await ctx.send(helpers.generate_openai_chat(" ".join(args)))
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
