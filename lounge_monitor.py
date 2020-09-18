import discord
from discord.ext import tasks, commands
from typing import List, Tuple, Dict
import os.path
import pickle
import time

import wiringpi
sensor_pin = 16

MSG_OPEN = 'Lounge is Open!'
MSG_CLOSED = 'Lounge is Closed.'
MSG_ERR = 'Not connected'

notify_list_name = 'lounge_monitor_notify.pkl'


class LoungeMonitor(commands.Cog):
    def __init__(self, bot: discord.Client, change_timeout=30):
        self.bot = bot
        self.last_change = -change_timeout
        self.change_timeout = change_timeout
        self.last_state = MSG_ERR

        wiringpi.wiringPiSetup()
        wiringpi.pinMode(sensor_pin, 0)

        try:
            self.notifs = pickle.load(open(notify_list_name, 'rb'))
        except (OSError, IOError):
            self.notifs = set()
            pickle.dump(self.notifs, open(notify_list_name, 'wb'))

    async def check_door(self):
        to_send = ''
        try:
            door_state = not wiringpi.digitalRead(sensor_pin)
            to_send = MSG_OPEN if door_state else MSG_CLOSED
        except:
            to_send = MSG_ERR

        if self.last_state != to_send:
            await self.bot.change_presence(activity=discord.Game(to_send))
            self.last_change = time.time()
            self.last_state = to_send
            return True
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        self.key_ch = self.bot.get_channel(756578279758102688)
        self.door_monitor.start()

    @commands.command()
    async def lounge(self, ctx: commands.Context):
        await self.check_door()
        await ctx.send(self.last_state)

    @tasks.loop(seconds=1)
    async def door_monitor(self):
        if self.last_change + self.change_timeout < time.time():
            changed = await self.check_door()
            if changed:
                self.broadcast()
            #     await self.key_ch.send(self.last_state)

    async def broadcast(self):
        for iid in self.notifs:
            self.bot.get_user(iid).send(self.last_state)

    @commands.command()
    async def sub(self, ctx: commands.Context):
        if ctx.author.id in self.notifs:
            await ctx.author.send('You\'re already in lol')
            return

        self.notifs.add(ctx.author.id)
        await ctx.author.send('You\'ll get a DM every time lounge state changes now. Have fun! (usub to stop)')
        pickle.dump(self.notifs, open(notify_list_name, 'wb'))

    @commands.command()
    def usub(self, ctx: commands.Context):
        if ctx.author.id in self.notifs:
            self.notifs.remove(ctx.author.id)
            pickle.dump(self.notifs, open(notify_list_name, 'wb'))
