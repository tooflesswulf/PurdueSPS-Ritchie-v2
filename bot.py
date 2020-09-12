import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Logged in as {}!'.format(client.user))

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
        s = ''
        for l in f.readlines():
            if len(s) + len(l) + 1 < 2000:
                s += l + '\n'
            else:
                ctx.send(s)
                s = l + '\n'
        if len(s) > 0:
            ctx.send(s)


with open('token.txt', 'r') as f:
    tok = f.readline()
    client.run(tok)
