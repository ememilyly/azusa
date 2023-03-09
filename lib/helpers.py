import logging
from configparser import ConfigParser
import os

_log = logging.getLogger(__name__)


def available_exts() -> list:
    exts = []
    for ext in os.listdir("cogs"):
        if ext.endswith(".py"):
            exts.append(ext[:-3])

    return exts


def reload_cfg(path) -> ConfigParser:
    config = ConfigParser()
    config.read(path)
    return config


def get_object_from_mention(ctx, mention):
    mentioned_id = int(mention[2:][:-1])
    if mention[1] == "@":
        return ctx.guild.get_member(mentioned_id)
    elif mention[1] == "#":
        return ctx.guild.get_channel_or_thread(mentioned_id)
        pass
