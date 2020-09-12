import discord
from discord.ext import commands
import util
import os, sys

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Logged in as {}!'.format(client.user))
    sys.stdout.flush()

    hello_ch = client.get_channel(754173414867992686)
    if hello_ch is not None:
        await hello_ch.send('(Re)starting bot!')


@client.command()
async def ping(ctx: discord.ext.commands.Context):
    await ctx.send('pong2')


@client.command()
async def log(ctx: discord.ext.commands.Context):
    if ctx.guild.id != 286028084287635456:
        return
    with open('log.txt', 'r') as f:
        lines = f.readlines()
        print(lines)
        sys.stdout.flush()
        for l in util.long_print(lines):
            await ctx.send(l)


@client.command()
async def err(ctx: discord.ext.commands.Context):
    if ctx.guild.id != 286028084287635456:
        return
    if not os.path.exists('logerr.txt'):
        return
    with open('logerr.txt', 'r') as f:
        for l in util.long_print(f.readlines()):
            await ctx.send(l)


with open('token.txt', 'r') as f:
    tok = f.readline()
    client.run(tok)
