from discord.ext import commands
import logging

import os

_log = logging.getLogger(__name__)


class Azusa(commands.Bot):

    @property
    def available_extensions(self) -> list:
        exts = []
        for ext in os.listdir(self.cogs_dir):
            if ext.endswith(".py"):
                exts.append(f"{self.cogs_dir}.{ext[:-3]}")

        return exts

    @property
    def commands_and_aliases(self) -> list:
        cmds = [cmd.name for cmd in self.commands]
        for cmd in self.commands:
            if cmd.aliases:
                cmds += [alias for alias in cmd.aliases]

        cmds.insert(0, "help")
        return cmds
