from discord.ext import commands
import logging
import os

from .helpers import *
from .invokers import *
from .methods import *
from .secrets import Secrets


_log = logging.getLogger(__name__)


class Persephone(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    log = _log
    current_activity = None

    @property
    def ext_dir(self) -> str:
        return __name__ + ".ext"

    @property
    def available_extensions(self) -> list:
        exts = []
        for ext in os.listdir(os.path.dirname(__file__) + "/ext"):
            if ext.endswith(".py"):
                exts.append(f"persephone.ext.{ext[:-3]}")

        return exts

    @property
    def commands_and_aliases(self) -> list:
        cmds = [cmd.name for cmd in self.commands]
        for cmd in self.commands:
            if cmd.aliases:
                cmds += [alias for alias in cmd.aliases]

        cmds.insert(0, "help")
        return cmds
