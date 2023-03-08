import os
import logging
from configparser import ConfigParser

_log = logging.getLogger(__name__)


async def log_command(instance, ctx):
    cmd = ctx.message.content.split(' ')
    instance.log.info(f'AUTHOR:{ctx.author.id} CMD:{cmd}')


def available_exts():
    exts = []
    for ext in os.listdir("cogs"):
        if ext.endswith(".py"):
            exts.append(ext[:-3])

    return exts


def reload_cfg(path):
    config = ConfigParser()
    config.read(path)
    return config
