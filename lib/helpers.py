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
