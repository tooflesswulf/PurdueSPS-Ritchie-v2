import discord
from discord.ext import commands
from typing import List, Tuple, Dict
import time

import wiringpi
sensor_pin = 16

MSG_OPEN = 'Lounge is Open!'
MSG_CLOSED = 'Lounge is Closed.'
MSG_ERR = 'Not connected'


class LoungeMonitor(commands.Cog):
    def __init__(self, bot: discord.Client, check_freq=5):
        self.bot = bot
        self.last_check = -check_freq
        self.check_freq = check_freq
        self.last_state = MSG_ERR

        wiringpi.wiringPiSetup()
        wiringpi.pinMode(sensor_pin, 0)

    async def check_door(self):
        self.last_check = time.time()

        to_send = ''
        try:
            door_state = not wiringpi.digitalRead(sensor_pin)
            to_send = MSG_OPEN if door_state else MSG_CLOSED
        except:
            to_send = MSG_ERR

        if self.last_state != to_send:
            await self.bot.change_presence(activity=discord.Game(to_send))
            self.last_state = to_send

    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_door()

    @commands.command()
    async def lounge(self, ctx: commands.Context):
        await self.check_door()
        await ctx.send(self.last_state)
