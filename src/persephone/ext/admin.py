from discord.ext import commands, tasks
import discord
import logging
import persephone

from functools import partial
import random
import re

_log = logging.getLogger(__name__)


class admin(commands.Cog):
    """Bot administration cog for managing bot things"""

    def __init__(self, bot):
        self.bot = bot
        self.log = _log
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(minutes=30.0)
    async def change_status(self):
        await self.status(None)

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()

    @commands.before_invoke(persephone.invokers.log_command)
    @commands.is_owner()
    @commands.command(aliases=("exts",), hidden=True)
    async def listexts(self, ctx):
        loaded_exts = self.bot.extensions.keys()
        unloaded_exts = []
        for ext in self.bot.available_extensions:
            if ext not in loaded_exts:
                unloaded_exts.append(ext)

        message = f"Loaded extensions:\n`{'`, `'.join(sorted(loaded_exts))}`"
        if unloaded_exts:
            message += "\n\nUnloaded extensions:\n`%s`" % "`, `".join(
                sorted(unloaded_exts)
            )

        await ctx.reply(message)

    @commands.before_invoke(persephone.invokers.log_command)
    @commands.is_owner()
    @commands.command(aliases=("cogs",), hidden=True)
    async def listcogs(self, ctx):
        message = "Loaded cogs:\n`" + "`, `".join(sorted(self.bot.cogs.keys())) + "`"
        await ctx.reply(message)

    @commands.before_invoke(
        partial(
            persephone.invokers.multiple,
            [persephone.invokers.log_command, persephone.invokers.check_alnum],
        )
    )
    @commands.is_owner()
    @commands.command(
        aliases=("load",), help="Load a space separated list of extensions", hidden=True
    )
    async def loadext(
        self,
        ctx,
        *,
        exts: str = commands.parameter(description="Which extensions to load"),
    ):
        _loaded = []
        _failed = []
        async with ctx.typing():
            for ext in exts.split(" "):
                if not ext.startswith(self.bot.ext_dir):
                    ext = f"{self.bot.ext_dir}.{ext}"
                try:
                    await self.bot.load_extension(ext)
                except commands.ExtensionNotFound:
                    _failed.append(f"{ext}?")
                except commands.ExtensionAlreadyLoaded:
                    _failed.append(f"{ext}!")
                except Exception as e:
                    self.log.error(f"Exception trying to load {ext}:")
                    self.log.error(e)
                    _failed.append(f"{ext}‽")
                else:
                    _loaded.append(ext)
        msg = ""
        if _loaded:
            msg += f"Loaded `{'`, `'.join(_loaded)}` :muscle:"
        if _failed:
            msg += f"\nFailed `{'`, `'.join(_failed)}` :frowning:"
        await ctx.reply(msg.strip())

    @commands.before_invoke(
        partial(
            persephone.invokers.multiple,
            [persephone.invokers.log_command, persephone.invokers.check_alnum],
        )
    )
    @commands.is_owner()
    @commands.command(
        aliases=("unload",),
        help="Unload a space separated list of extensions",
        hidden=True,
    )
    async def unloadext(
        self,
        ctx,
        *,
        exts: str = commands.parameter(description="Which extensions to unload"),
    ):
        _unloaded = []
        _failed = []
        for ext in exts.split(" "):
            if not ext.startswith(self.bot.ext_dir):
                ext = f"{self.bot.ext_dir}.{ext}"
            try:
                await self.bot.unload_extension(ext)
            except commands.ExtensionNotLoaded:
                _failed.append(f"{ext}?")
            except Exception as e:
                self.log.error(f"Exception trying to unload {ext}:")
                self.log.error(e)
                _failed.append(f"{ext}‽")
            else:
                _unloaded.append(ext)
        msg = ""
        if _unloaded:
            msg += f"Unloaded `{'`, `'.join(_unloaded)}` :muscle:"
        if _failed:
            msg += f"Failed `{'`, `'.join(_failed)}` :frowning:"
        await ctx.reply(msg.strip())

    @commands.before_invoke(
        partial(
            persephone.invokers.multiple,
            [persephone.invokers.log_command, persephone.invokers.check_alnum],
        )
    )
    @commands.is_owner()
    @commands.command(hidden=True)
    async def reload(
        self,
        ctx,
        *,
        exts: str = commands.parameter(
            default=None,
            description="Which extensions to reload, if empty reloads everything",
        ),
    ):
        if not exts:
            # Reload everything
            exts = ' '.join(list(self.bot.extensions.keys()))

        _reloaded = []
        _failed = []
        for ext in exts.split(" "):
            if not ext.startswith(self.bot.ext_dir):
                ext = f"{self.bot.ext_dir}.{ext}"
            try:
                await self.bot.reload_extension(ext)
            except Exception as e:
                self.log.error(f"Exception trying to reload {ext}:")
                self.log.error(e)
                _failed.append(ext)
            else:
                _reloaded.append(ext)
        msg = ""
        if _reloaded:
            msg += f"Reloaded `{'`, `'.join(_reloaded)}` :muscle:"
        if _failed:
            msg += f"\nFailed `{'`, `'.join(_failed)}` :frowning:"
        await ctx.reply(msg)

    @commands.before_invoke(persephone.invokers.log_command)
    @commands.is_owner()
    @commands.command(hidden=True)
    async def status(self, ctx):
        activities = {
            "playing": discord.ActivityType.playing,
            "listening to": discord.ActivityType.listening,
            "watching": discord.ActivityType.watching,
        }
        activity = random.choice([i for i in activities.keys()])
        prompt = f"generate a short one sentence status for what you are doing starting with the word {activity}"
        activity_text = await persephone.helpers.generate_openai_chat(prompt)
        # Change response like '@persephone-dev Listening to whatever i like'
        # to just 'whatever i like' as openai can add some fluff
        regex = "(?i)(?:listening to|playing|watching)\\s+(.*)"
        activity_text = re.search(regex, activity_text)[1]
        self.log.info(f"New status: {activity} {activity_text}")
        self.bot.current_activity = f"{activity} {activity_text}"
        await self.bot.change_presence(
            activity=discord.Activity(type=activities[activity], name=activity_text),
            status=self.bot.status,
        )

    @loadext.error
    @unloadext.error
    @reload.error
    async def ext_command_handler(self, ctx, e):
        if isinstance(e, commands.MissingRequiredArgument):
            if e.param.name == "exts":
                await ctx.reply(
                    "Am I supposed to know which extensions you want? :unamused:"
                )
        elif isinstance(e, commands.UserInputError):
            await ctx.message.add_reaction("😡")
        else:
            await ctx.message.add_reaction("❌")
            raise e


async def setup(bot):
    _log.info(f"loading {__name__}")
    await bot.add_cog(admin(bot))
