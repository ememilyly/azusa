from discord.ext import commands
import logging

import os

_log = logging.getLogger(__name__)


class Azusa(commands.Bot):
    pass

    @property
    def available_exts(self) -> list:
        if not self.config:
            path = "cogs"
        else:
            path = self.config["bot"]["ext_dir"]
        exts = []
        for ext in os.listdir(path):
            if ext.endswith(".py"):
                exts.append(ext[:-3])

        return exts

    @property
    def commands_and_aliases(self) -> list:
        cmds = [cmd.name for cmd in self.commands]
        for cmd in self.commands:
            if cmd.aliases:
                cmds += [alias for alias in cmd.aliases]

        cmds.append("help")
        return cmds
