import os
import logging
from configparser import ConfigParser

_log = logging.getLogger(__name__)

def available_exts():
    exts = []
    for ext in os.listdir('cogs'):
        if ext.endswith('.py'):
            exts.append(ext[:-3])

    return exts

def reload_cfg(path):
    config = ConfigParser()
    config.read(path)
    return config
