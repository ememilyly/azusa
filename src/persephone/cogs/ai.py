from discord.ext import commands
import discord
from lib import helpers
import logging

import requests

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
                    await message.reply(
                        helpers.generate_openai_chat(message.clean_content)
                    )
            elif message.type == discord.MessageType.reply:
                # prompt = f"'{message.author.display_name}' replied to you but the message they replied to was from so long ago you forgot what it was"
                # message.mentions allows to turn off mentions and she won't reply
                if message.reference.cached_message and message.mentions:
                    if message.reference.cached_message.author.id == self.bot.user.id:
                        prompt = [{"role": "user", "content": message.clean_content}]
                        ref_msg = message.reference.cached_message
                        # follow ref chain as far as we can go up for conversation
                        while True:
                            content = ref_msg.clean_content
                            if ref_msg.author.id == self.bot.user.id:
                                role = "assistant"
                            else:
                                role = "user"
                            prompt.insert(0, {"role": role, "content": content})
                            if ref_msg.type == discord.MessageType.reply:
                                if ref_msg.reference.cached_message:
                                    # go again
                                    ref_msg = ref_msg.reference.cached_message
                                    continue
                            break
                        async with message.channel.typing():
                            await message.reply(helpers.generate_openai_chat(prompt))

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
                except requests.exceptions.ReadTimeout:
                    await ctx.message.add_reaction("❌")
                    await ctx.message.add_reaction("⏱")
                    return
                except Exception as e:
                    await ctx.message.add_reaction("❌")
                    raise e
                await ctx.reply(
                    file=discord.File(image, filename="image.png", spoiler=True)
                )
        else:
            prompt = f"i ({ctx.author.display_name}) asked you to generate an image but you need to know what the image would be of and i didn't tell you"

            async with ctx.typing():
                await ctx.reply(helpers.generate_openai_chat(prompt))

    @commands.command()
    async def t2imodels(self, ctx):
        models = helpers.get_dezgo_models()
        await ctx.paged_reply(self.bot, models)


async def setup(bot):
    _log.info(f"loading {__name__}")
    # TODO: move this to stop loading just the command?
    if bot.config["ai"]["openai_api_key"]:
        await bot.add_cog(ai(bot))
    else:
        e = "no openai api key found, not loading"
        _log.warning(e)
        raise commands.ExtensionError(e, name=__name__)
