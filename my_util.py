from discord.ext import commands
from typing import List, Iterator

# Formats a bunch of lines into a list of lines<2000 chars
def long_print(lines: List[str]) -> Iterator[str]:
    s = ''
    for l in lines:
        if len(s) + len(l) < 2000:
            s += l
        else:
            yield s
            s = l
    if len(s) != 0:
        yield s

def in_guild(guild_id: int):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)
