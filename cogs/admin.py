from discord.ext import commands
from time import sleep

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prune(self, ctx, *args):
        if ctx.author.permissions_in(ctx.channel).manage_messages and args[0].isdigit():
            # smol limit because discord rate limits
            limit = 10
            if limit > int(args[0]): limit = args[0]
            async for message in ctx.channel.history(limit=int(args[0])+1):
                await message.delete()

        if ctx.author.id == 651651128521523210:
            await ctx.send('F O R F R E E')
            sleep(1) 

def setup(bot):
    bot.add_cog(Admin(bot))
