import itertools
import datetime
import disnake
from disnake.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

from .info import Info
from .math import Math
from .pvc import PrivateVC
from .wordle import Wordle
from .teacher import Lee
from .tictactoe import TicTacToe
from .counting_logger import Counting
from .image import image_handler
from .scrapper import Scrapper
from .testing_disnake import Testing


class FunBot(commands.Bot):
    intents = disnake.Intents.default()
    intents.members = True

    def __init__(self):
        self.prefix = ['f ', "f."]
        super().__init__(command_prefix=self.prefix)
        self.statuss = itertools.cycle([f'{self.prefix[0]}help', 'with your mom', f'{self.prefix[0]}help'])
        self.remove_command('help')
        self.intents = FunBot.intents

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.change_presence(activity=disnake.Game(next(self.statuss)))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print(f"{self.user.name} is ready")


