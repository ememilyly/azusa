import logging

import asyncio

_log = logging.getLogger(__name__)


async def paged_reply(self, bot, content):
    # https://stackoverflow.com/a/61786852
    per_page = 10
    pages = int(len(content) / per_page) + 1
    cur_page = 1
    chunk = content[:per_page]
    page_content = "Page `%s/%s`:\n```ini\n%s```"
    message = await self.send(page_content % (cur_page, pages, '\n'.join(chunk)))
    # terminal doesn't like these and cba to fix fonts and stuff
    await message.add_reaction("\u25c0")  # ◀️
    await message.add_reaction("\u25b6")  # ▶️

    def check(reaction, user):
        return user == self.author and str(reaction.emoji) in ["\u25c0", "\u25b6"]

    while True:
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60, check=check
            )

            if str(reaction.emoji) == "\u25b6":
                if cur_page == pages:
                    # loop around
                    cur_page = 1
                else:
                    cur_page += 1
                if cur_page != pages:
                    chunk = content[(cur_page - 1) * per_page: cur_page * per_page]
                else:
                    chunk = content[(cur_page - 1) * per_page:]
                await message.edit(
                    content=page_content % (cur_page, pages, '\n'.join(chunk))
                )
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "\u25c0":
                if cur_page == 1:
                    cur_page = pages
                else:
                    cur_page -= 1
                chunk = content[(cur_page - 1) * per_page: cur_page * per_page]
                await message.edit(
                    content=page_content % (cur_page, pages, '\n'.join(chunk))
                )
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            break
