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


with open('token.txt', 'r') as f:
    tok = f.readline()
    client.run(tok)
