from discord.ext import commands
from lib import helpers
import logging

_log = logging.getLogger(__name__)


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = _log

    @property
    def _loaded_extensions(self):
        # ['cogs.example'] -> ['example']
        # maybe will just use what discord.py gives at some point but for now
        # this makes life easier, all my stuff is in one folder
        return [ext.split(".")[1] for ext in self.bot.extensions.keys()]

    @commands.before_invoke(helpers.log_command)
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
        for ext in helpers.available_exts():
            if ext not in loaded_exts:
                unloaded_exts.append(ext)

        message = "Loaded extensions:\n`" + "`, `".join(sorted(loaded_exts)) + "`"
        if unloaded_exts:
            message +=  \
                "\n\nUnloaded extensions:\n`" + "`, `".join(sorted(unloaded_exts)) + "`"

        await ctx.send(message)

    @commands.before_invoke(helpers.log_command)
    @commands.is_owner()
    @commands.command(
        aliases=(
            "load",
        ),
        hidden=True
    )
    async def loadext(self, ctx, *args):
        if not args:
            await ctx.send("Please specify which extensions to load.")
        else:
            _available_exts = helpers.available_exts()
            for ext in args:
                if ext not in _available_exts:
                    await ctx.send(f"Can't find `{ext}` :frowning:")
                elif ext in self._loaded_extensions:
                    await ctx.send(f"`{ext}` is already loaded.")
                else:
                    try:
                        await self.bot.load_extension(f"cogs.{ext}")
                    except Exception as e:
                        self.log.error(f"Failed to load {ext}:")
                        self.log.error(e)
                        await ctx.send(f"Failed to load {ext} :sob:\n```{e}```")
                    else:
                        await ctx.send(f"Loaded `{ext}` :muscle:")

    @commands.before_invoke(helpers.log_command)
    @commands.is_owner()
    @commands.command(
        aliases=(
            "unload",
        ),
        hidden=True
    )
    async def unloadext(self, ctx, *args):
        if not args:
            await ctx.send("Please specify which extensions to unload.")
        else:
            _loaded_exts = self._loaded_extensions
            for ext in args:
                if ext not in _loaded_exts:
                    await ctx.send(f"Unknown extension `{ext}` :frowning:")
                else:
                    await self.bot.unload_extension(f"cogs.{ext}")
                    await ctx.send(f"Unloaded `{ext}` :wave:")

    @commands.before_invoke(helpers.log_command)
    @commands.is_owner()
    @commands.command(
        aliases=(
            "reload",
        ),
        hidden=True
    )
    async def reloadcog(self, ctx, *args):
        if not args:
            exts = sorted(self._loaded_extensions)
            for ext in exts:
                await self.bot.reload_extension(f"cogs.{ext}")
            await ctx.send(
                f"{len(self.bot.extensions)} extensions reloaded:"
                f'`{"`, `".join(exts)}`'
            )
            self.bot.config = helpers.reload_cfg("bot.cfg")
            self.bot.command_prefix = self.bot.config["bot"]["prefix"]
            await ctx.send("Reloaded config :muscle:")
        else:
            for ext in args:
                if ext in ("cfg", "config"):
                    self.bot.config = helpers.reload_cfg("bot.cfg")
                    self.bot.command_prefix = self.bot.config["bot"]["prefix"]
                    await ctx.send("Reloaded config :slight_smile:")
                elif ext in self.bot.cogs.keys():
                    await self.bot.reload_extension(f"cogs.{ext.lower()}")
                    await ctx.send(f"Reloaded `{ext}` :muscle:")
                else:
                    await ctx.send(f"Unknown extension `{ext}` :frowning:")

    @commands.before_invoke(helpers.log_command)
    @commands.is_owner()
    @commands.command(
        hidden=True
    )
    # TODO
    async def log(self, ctx, *args):
        pass


async def setup(bot):
    _log.info(f"loading {__name__}")
    await bot.add_cog(admin(bot))
