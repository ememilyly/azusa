import logging

import asyncio
import math

_log = logging.getLogger(__name__)


async def paged_reply(self, bot, content):
    # https://stackoverflow.com/a/61786852
    per_page = 10
    pages = math.ceil(len(content) / per_page)
    cur_page = 1
    chunk = content[:per_page]
    linebreak = "\n"
    message = await self.send(f"Page {cur_page}/{pages}:\n```{linebreak.join(chunk)}```")
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    active = True

    def check(reaction, user):
        return user == self.author and str(reaction.emoji) in ["◀️", "▶️"]
        # or you can use unicodes, respectively: "\u25c0" or "\u25b6"

    while active:
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60, check=check
            )

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                if cur_page != pages:
                    chunk = content[(cur_page - 1) * per_page: cur_page * per_page]
                else:
                    chunk = content[(cur_page - 1) * per_page:]
                await message.edit(
                    content=f"Page {cur_page}/{pages}:\n```{linebreak.join(chunk)}```"
                )
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                chunk = content[(cur_page - 1) * per_page: cur_page * per_page]
                await message.edit(
                    content=f"Page {cur_page}/{pages}:\n```{linebreak.join(chunk)}```"
                )
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            active = False
