from discord.ext import commands
import discord
import logging
from configparser import ConfigParser

import os
import re
import requests

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


def replace_mentions_with_names(ctx: commands.Context, args: str) -> str:
    text = []
    for word in args.split(" "):
        mention_regex = "^<(@|#)\\d*>$"
        # e.g. <@111222333444555666>
        if re.match(mention_regex, word):
            obj = get_object_from_mention(ctx, word)
            if isinstance(obj, discord.Member):
                if obj.nick:
                    word = obj.nick
                else:
                    word = obj.name
            else:
                word = obj.name
        text.append(word)

    return " ".join(text)


def get_object_from_mention(ctx: commands.Context, mention: str):
    mentioned_id = int(mention[2:][:-1])
    if mention[1] == "@":
        return ctx.guild.get_member(mentioned_id)
    elif mention[1] == "#":
        return ctx.guild.get_channel_or_thread(mentioned_id)
        pass


def generate_openai_chat(
    prompt: str,
    key: str,
    model: str = "gpt-3.5-turbo"
) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "your name is azusa and you're a moody and very rude teenage girl chat bot who never says sorry and calls people bitch a lot."},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    r = requests.post(url, json=data, headers=headers)

    _log.debug(r.json())

    return r.json()["choices"][0]["message"]["content"]


def generate_rude_response_missing_arg(victim: str, key: str) -> str:
    prompt = f"you were asked to run a command by {victim} but not given all the arguments to do so"

    return generate_openai_chat(prompt, key)
