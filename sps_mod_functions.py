import discord
from discord.ext import commands
from typing import List, Tuple, Dict
import time
from datetime import date

import my_util


class ModFunctions(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.quiet_list: Dict[int, float] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        # self.guild = 481808675346841600
        self.guild = self.bot.get_guild(286028084287635456)
        
        self.admin_ch = self.bot.get_channel(691491919808823326)
        self.join_log = self.bot.get_channel(691491919808823326)
        self.join_role = self.guild.get_role(691840210631262248)

    def cog_check(self, ctx: commands.Context):
        return ctx.guild == self.guild and ctx.author.guild_permissions.kick_members

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild != self.guild:
            return
        await member.add_roles(self.join_role)
        print('Added role Temporary Member to {}'.format(member.display_name))

        await member.send('Hey there! Thanks for joining the Purdue SPS server. '
                          + 'We\'re glad to have you.\nIf you wouldn\'t mind, '
                          + 'please change your server nickname to your first '
                          + 'and/or last name. If you\'re having trouble with this, '
                          + 'ask one of the administrators for help. Thanks!')
        await self.join_log.send('{} - {}'.format(member.mention, date.today().strftime('%d %b %Y')))

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild != self.guild:
            return
        await self.admin_ch.send('A person left: {}'.format(member.mention))

    @commands.command()
    async def quiet(self, ctx: commands.Context, member: discord.Member, dur: float):
        await ctx.send('Silenced {} for {}s'.format(member.mention, int(dur)))
        self.quiet_list[member.id] = time.time() + dur

    async def bot_check(self, ctx: commands.Context):
        if ctx.author.id in self.quiet_list:
            return self.quiet_list[ctx.author.id] < time.time()
        return True

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.guild is None or msg.guild != self.guild:
            return
        if msg.author.id in self.quiet_list:
            if self.quiet_list[msg.author.id] > time.time():
                await msg.delete()
            else:
                del self.quiet_list[msg.author.id]
