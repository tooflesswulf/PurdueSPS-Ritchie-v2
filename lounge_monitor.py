import discord
from discord.ext import tasks, commands
from typing import List, Tuple, Dict
import time

import wiringpi
sensor_pin = 16

MSG_OPEN = 'Lounge is Open!'
MSG_CLOSED = 'Lounge is Closed.'
MSG_ERR = 'Not connected'


class LoungeMonitor(commands.Cog):
    def __init__(self, bot: discord.Client, change_timeout=30):
        self.bot = bot
        self.last_change = -change_timeout
        self.change_timeout = change_timeout
        self.last_state = MSG_ERR

        wiringpi.wiringPiSetup()
        wiringpi.pinMode(sensor_pin, 0)

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
        self.key_ch = await self.bot.get_channel(756578279758102688)
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
                self.key_ch.send(self.last_state)
