import itertools

import discord
from discord.ext import commands, tasks
from discord_components import DiscordComponents
from dotenv import load_dotenv
import os

load_dotenv()

from .info import Info
from .math import Math
from .pvc import PrivateVC
from .wordle import Wordle
from .teacher import Lee
from .tictactoe import TicTacToe
from .counting_logger import Counting
from .image import image_handler


class FunBot(commands.Bot):
    intents = discord.Intents.default()
    intents.members = True

    def __init__(self):
        self.prefix = 'f.'
        super().__init__(command_prefix=self.prefix)
        self.status = itertools.cycle([f'{self.prefix}help', 'with your mom', f'{self.prefix}help'])
        self.remove_command('help')
        self.intents = FunBot.intents

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.change_presence(activity=discord.Game(next(self.status)))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print(f"{self.user.name} is ready")
        DiscordComponents(self)
