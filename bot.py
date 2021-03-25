import discord
from discord.ext import commands

import builtins
import typing
import sys
import os

from sps_mod_functions import ModFunctions
import my_util

client = commands.Bot(command_prefix='!')
if not (len(sys.argv) > 1 and sys.argv[1] == 'DEBUG'):
    client.add_cog(ModFunctions(client))

    from lounge_monitor import LoungeMonitor
    client.add_cog(LoungeMonitor(client))


@client.event
async def on_ready():
    print('Logged in as {}!'.format(client.user))
    sys.stdout.flush()

    hello_ch = client.get_channel(754173414867992686)
    if hello_ch is not None:
        await hello_ch.send('(Re)starting bot!')

    nepo = client.get_channel(481813325332873217)
    if nepo is not None:
        await nepo.send('Updating Albert version 21.... Done!')


@client.command()
@my_util.in_guild(286028084287635456)
async def log(ctx: discord.ext.commands.Context):
    sys.stdout.flush()
    with open('log.txt', 'r') as f:
        lines = f.readlines()
        for l in my_util.long_print(lines):
            await ctx.send(l)


@client.command()
@my_util.in_guild(286028084287635456)
async def err(ctx: discord.ext.commands.Context):
    if not os.path.exists('logerr.txt'):
        return
    with open('logerr.txt', 'r') as f:
        for l in my_util.long_print(f.readlines()):
            await ctx.send(l)


@client.command()
@my_util.in_guild(286028084287635456)
async def reboot(ctx: discord.ext.commands.Context):
    exit(0)


if __name__ == '__main__':
    with open('token.txt', 'r') as f:
        tok = f.readline()
        client.run(tok)
