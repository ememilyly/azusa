from discord.ext import commands
import logging

_log = logging.getLogger(__name__)


async def multiple(functions, *args):
    for f in functions:
        await f(*args)


async def log_command(
    instance: commands.Cog,
    ctx: commands.context.Context
):
    cmd = ctx.message.content.split(' ')
    instance.log.info(f'AUTHOR:{ctx.author.id} CMD:{cmd}')


async def check_alnum(
    instance: commands.Cog,
    ctx: commands.context.Context
):
    # Remove base command from message
    args = ''.join(ctx.message.content.split(' ')[1:])
    if args:
        if not args.isalnum():
            raise commands.UserInputError('Arguments must be alphanumeric')
