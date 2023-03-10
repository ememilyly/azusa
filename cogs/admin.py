from discord.ext import commands
from lib import helpers, invokers
import logging

from functools import partial

_log = logging.getLogger(__name__)


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @property
    def _loaded_extensions(self) -> list:
        # ['cogs.example'] -> ['example']
        # maybe will just use what discord.py gives at some point but for now
        # this makes life easier, all my stuff is in one folder
        return [ext.split(".")[1] for ext in self.bot.extensions.keys()]

    @commands.before_invoke(invokers.log_command)
    @commands.is_owner()
    @commands.command(
        aliases=(
            "listextensions",
            "exts",
            "listcogs",
            "cogs",
        ),
        hidden=True
    )
    async def listexts(self, ctx):
        loaded_exts = self._loaded_extensions
        unloaded_exts = []
        for ext in self.bot.available_exts:
            if ext not in loaded_exts:
                unloaded_exts.append(ext)

        message = "Loaded extensions:\n`" + "`, `".join(sorted(loaded_exts)) + "`"
        if unloaded_exts:
            message +=  \
                "\n\nUnloaded extensions:\n`" + "`, `".join(sorted(unloaded_exts)) + "`"

        await ctx.reply(message)

    @commands.before_invoke(partial(
        invokers.multiple,
        [
            invokers.log_command,
            invokers.check_alnum
        ]
    ))
    @commands.is_owner()
    @commands.command(
        aliases=(
            "load",
        ),
        help="Load a space separated list of extensions",
        hidden=True
    )
    async def loadext(
        self,
        ctx,
        *,
        exts: str = commands.parameter(
            description="Which extensions to load"
        )
    ):
        if exts:
            _available_exts = self.bot.available_exts
            for ext in exts.split(' '):
                if ext not in _available_exts:
                    await ctx.reply(f"Can't find `{ext}` :frowning:")
                elif ext in self._loaded_extensions:
                    await ctx.reply(f"`{ext}` is already loaded.")
                else:
                    try:
                        # TODO: change these references to pick up from config
                        await self.bot.load_extension(f"cogs.{ext}")
                    except Exception as e:
                        self.log.error(f"Failed to load {ext}:")
                        self.log.error(e)
                        await ctx.reply(f"Failed to load {ext} :sob:\n```{e}```")
                    else:
                        await ctx.reply(f"Loaded `{ext}` :muscle:")
        else:
            await ctx.reply("Please specify which extensions to load.")

    @commands.before_invoke(partial(
        invokers.multiple,
        [
            invokers.log_command,
            invokers.check_alnum
        ]
    ))
    @commands.is_owner()
    @commands.command(
        aliases=(
            "unload",
        ),
        help="Unload a space separated list of extensions",
        hidden=True
    )
    async def unloadext(
        self,
        ctx,
        *,
        exts: str = commands.parameter(
            description="Which extensions to unload"
        )
    ):
        if exts:
            _loaded_exts = self._loaded_extensions
            for ext in exts.split(' '):
                if ext not in _loaded_exts:
                    await ctx.reply(f"Unknown extension `{ext}` :frowning:")
                else:
                    await self.bot.unload_extension(f"cogs.{ext}")
                    await ctx.reply(f"Unloaded `{ext}` :wave:")
        else:
            await ctx.reply("Please specify which extensions to unload.")

    @commands.before_invoke(partial(
        invokers.multiple,
        [
            invokers.log_command,
            invokers.check_alnum
        ]
    ))
    @commands.is_owner()
    @commands.command(
        aliases=(
            "reload",
        ),
        hidden=True
    )
    async def reloadext(
        self,
        ctx,
        *,
        exts: str = commands.parameter(
            default=None,
            description="Which extensions to reload, if empty reloads everything"
        )
    ):
        if not exts:
            # Reload everything
            exts = sorted(self._loaded_extensions)
            for ext in exts:
                await self.bot.reload_extension(f"cogs.{ext}")
            await ctx.reply(
                f"{len(self.bot.extensions)} extensions reloaded: "
                f'`{"`, `".join(exts)}`'
            )
            self.bot.config = helpers.reload_cfg("bot.cfg")
            self.bot.command_prefix = self.bot.config["bot"]["prefix"]
            await ctx.reply("Reloaded config :muscle:")

        else:
            for ext in exts.split(' '):
                if ext in ("cfg", "config"):
                    self.log.info("loading config")
                    self.bot.config = helpers.reload_cfg("bot.cfg")
                    message = "Reloaded config :slight_smile:"
                    if self.bot.command_prefix != self.bot.config["bot"]["prefix"]:
                        self.log.info(
                            f"prefix changed to {self.bot.config['bot']['prefix']}"
                        )
                        self.bot.command_prefix = self.bot.config["bot"]["prefix"]
                        message += f" Use `{self.bot.command_prefix}cmd` now!"
                    await ctx.reply(message)
                elif ext in self.bot.cogs.keys():
                    await self.bot.reload_extension(f"cogs.{ext.lower()}")
                    await ctx.reply(f"Reloaded `{ext}` :muscle:")
                else:
                    await ctx.reply(f"Unknown extension `{ext}` :frowning:")

    @commands.before_invoke(invokers.log_command)
    @commands.is_owner()
    @commands.command(
        hidden=True
    )
    # TODO
    async def log(self, ctx, *args):
        pass

    @loadext.error
    @unloadext.error
    @reloadext.error
    async def ext_command_handler(self, ctx, e):
        if isinstance(e, commands.MissingRequiredArgument):
            if e.param.name == "exts":
                await ctx.reply("Am I supposed to know which extensions you want? :unamused:")
        elif isinstance(e, commands.UserInputError):
            await ctx.message.add_reaction("😡")


async def setup(bot):
    _log.info(f"loading {__name__}")
    await bot.add_cog(admin(bot))
