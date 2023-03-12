from discord.ext import commands
from lib import helpers, invokers
import logging

from functools import partial

_log = logging.getLogger(__name__)


class admin(commands.Cog):
    """Bot administration cog for managing bot things"""

    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    def reload_config(self) -> str:
        self.log.info("loading config")
        self.bot.config = helpers.reload_cfg("bot.cfg")
        message = "Reloaded config :slight_smile:"
        if self.bot.command_prefix != self.bot.config["bot"]["prefix"]:
            self.log.info(
                f"prefix changed to {self.bot.config['bot']['prefix']}"
            )
            self.bot.command_prefix = self.bot.config["bot"]["prefix"]
            message += f" Use `{self.bot.command_prefix}cmd` now!"

        return message

    @commands.before_invoke(invokers.log_command)
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

    @commands.before_invoke(invokers.log_command)
    @commands.is_owner()
    @commands.command(aliases=("cogs",), hidden=True)
    async def listcogs(self, ctx):
        message = "Loaded cogs:\n`" + "`, `".join(sorted(self.bot.cogs.keys())) + "`"
        await ctx.reply(message)

    @commands.before_invoke(
        partial(invokers.multiple, [invokers.log_command, invokers.check_alnum])
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
        for ext in exts.split(" "):
            if not ext.startswith(self.bot.cogs_dir):
                ext = f"{self.bot.cogs_dir}.{ext}"
            try:
                await self.bot.load_extension(ext)
            except commands.ExtensionNotFound:
                await ctx.reply("i dont have that loaded dumbass")
            except commands.ExtensionAlreadyLoaded:
                await ctx.reply("i already loaded that dumbass")
            except Exception as e:
                raise e
            else:
                await ctx.reply(f"Loaded `{ext}` :muscle:")

    @commands.before_invoke(
        partial(invokers.multiple, [invokers.log_command, invokers.check_alnum])
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
        for ext in exts.split(" "):
            if not ext.startswith(self.bot.cogs_dir):
                ext = f"{self.bot.cogs_dir}.{ext}"
            try:
                await self.bot.unload_extension(ext)
            except commands.ExtensionNotLoaded:
                await ctx.reply("idk what ur talking about dumbass")
            except Exception as e:
                raise e
            else:
                await ctx.reply(f"Unloaded `{ext}` :wave:")

    @commands.before_invoke(
        partial(invokers.multiple, [invokers.log_command, invokers.check_alnum])
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
            for ext in self.bot.extensions.keys():
                try:
                    await self.bot.reload_extension(ext)
                except Exception as e:
                    raise e
            await ctx.reply(
                f"{len(self.bot.extensions)} extensions reloaded: "
                f'`{"`, `".join(self.bot.extensions.keys())}`'
            )
            await ctx.reply(self.reload_config())

        else:
            for ext in exts.split(" "):
                if ext in ("cfg", "config"):
                    await ctx.reply(self.reload_config())
                else:
                    if not ext.startswith(self.bot.cogs_dir):
                        ext = f"{self.bot.cogs_dir}.{ext}"
                    try:
                        await self.bot.reload_extension(ext)
                    except Exception as e:
                        raise e
                    await ctx.reply(f"Reloaded `{ext}` :muscle:")

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
