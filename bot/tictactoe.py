import discord
from discord.ext import commands
from discord_components import ActionRow, Button, ButtonStyle
import random


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tic")
    async def tictactoe(self, ctx, person: discord.Member):
        game = TicTacToeGame(ctx.author, person, self.bot)
        await game.play(ctx)


# noinspection PyTypeChecker
class TicTacToeGame():
    def __init__(self, player1, player2, bot: commands.Bot):
        self.bot = bot
        self.amount = 0
        self.current_channel = None
        self.player1 = player1
        self.player2 = player2
        self.turn = -1
        self.position = -1
        self.main_msg = ""
        self.grid = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]
        self.x_amount = 0
        self.o_amount = 0
        self.yes_msg = False
        self.winning_letter = None


    async def the_grid(self):

        row = None
        if 0 <= self.position < 3:
            row = 0
        elif 3 <= self.position < 6:
            row = 1
        elif 6 <= self.position < 9:
            row = 2
        else:
            row = -1

        for i in range(3):
            for k in range(3):
                if self.grid[i][k] == 0:
                    self.grid[i][k] = self.starting()
                if self.turn == 1:
                    self.grid[row][self.position % 3] = self.o()
                elif self.turn == 2:
                    self.grid[row][self.position % 3] = self.x()



    def valid(self, current_os):
        copy_grd = [[" ", " ", " "],
                     [" ", " ", " "],
                     [" ", " ", " "]]
        print(f"grid: {self.grid}")
        for i in range(3):
            for k in range(3):
                if self.grid[i][k].label != " ":
                    copy_grd[i][k] = self.grid[i][k].label
        print(f"copy grid:{copy_grd}")

        for i in range(3):
            if copy_grd[i][0] == copy_grd[i][1] == copy_grd[i][2] != ' ':
                self.winning_letter = str(copy_grd[i][0])
                return True
            elif copy_grd[0][i] == copy_grd[1][i] == copy_grd[2][i] != ' ':
                self.winning_letter = str(copy_grd[0][i])
                return True
        if copy_grd[0][0] == copy_grd[1][1] == copy_grd[2][2] != ' ' or copy_grd[0][2] == copy_grd[1][1] == copy_grd[2][0] != ' ':
            self.winning_letter = str(copy_grd[1][1])
            return True
        if current_os == 0:
            return False
        return "not"




    async def play(self, ctx):

        rows = await self.rows()
        ran = random.randint(1, 2)
        self.main_msg = f"{self.player1.mention} vs. {self.player2.mention}\n "
        msg = f"{self.player1.mention} vs. {self.player2.mention}\n {self.player1.mention} goes first!"
        if ran == 1:
            msg = f"{self.player1.mention} vs. {self.player2.mention}\n {self.player1.mention} goes first!"
            self.turn = 1
        if ran == 2:
            msg = f"{self.player1.mention} vs. {self.player2.mention}\n {self.player2.mention} goes first!"
            self.turn = 2
        self.current_channel = ctx.channel
        await ctx.send(msg, components=rows)
        # --------------------------------------------------------------------------------
        for k in range(9):
            i = await self.bot.wait_for("button_click", check=lambda i: i.message.channel == self.current_channel)

            position = str(i.component.custom_id)
            position = int(position[0])


            if i.author == self.player1 or i.author == self.player2:

                if i.author == self.player1 and self.turn == 1:
                    self.position = position
                    rows = await self.rows()

                    if self.yes_msg is False:
                        msg = self.update()
                    elif self.yes_msg is True:
                        msg = self.main_msg
                        if self.winning_letter == "X":
                            msg += f"{self.player2.mention} won!"
                        elif self.winning_letter == "O":
                            msg += f"{self.player1.mention} won!"
                    elif self.yes_msg == "tie":
                        msg = self.main_msg
                        msg += f"**it's a tie!**"

                    await i.edit_origin(content=msg, components=rows)
                elif i.author == self.player2 and self.turn == 2:
                    self.position = position
                    rows = await self.rows()

                    if self.yes_msg is False:
                        msg = self.update()
                    elif self.yes_msg is True:
                        msg = self.main_msg
                        if self.winning_letter == "X":
                            msg += f"{self.player2.mention}"
                        elif self.winning_letter == "O":
                            msg += f"{self.player1.mention}"
                    elif self.yes_msg == "tie":
                        msg = self.main_msg
                        msg += f"**it's a tie!**"

                    await i.edit_origin(content=msg, components=rows)

                else:
                    await i.respond(content="Its not your turn!")
            else:
                await i.respond(content="Hey buddy, this ain't your game")

            current_os = 0
            for j in range(3):
                for m in range(3):
                    if self.grid[j][m].label == " ":
                        current_os += 1
            thing = self.valid(current_os)

            if thing is True:
                self.yes_msg = True

            if thing is False:
                self.yes_msg = "tie"

            if thing == "not":
                self.yes_msg = False

        if self.yes_msg is False:
            msg = self.update()
        elif self.yes_msg is True:
            msg = self.main_msg
            if self.winning_letter == "X":
                msg += f"{self.player2.mention}"
            elif self.winning_letter == "O":
                msg += f"{self.player1.mention}"
        elif self.yes_msg == "tie":
            msg = self.main_msg
            msg += f"**it's a tie!**"
        # --------------------------------------------------------------------------------

    async def rows(self):
        await self.the_grid()
        rows = self.grid
        rowss = [ActionRow(rows[0][0], rows[0][1], rows[0][2]),
                 ActionRow(rows[1][0], rows[1][1], rows[1][2]),
                 ActionRow(rows[2][0], rows[2][1], rows[2][2])]
        return rowss

    def update(self):
        msg = self.main_msg
        if self.turn == 1:
            self.turn = 2
            msg += f"It's now {self.player2.mention}'s turn"
        elif self.turn == 2:
            self.turn = 1
            msg += f"It's now {self.player1.mention}'s turn"
        return msg

    def starting(self):
        button = Button(label=" ", custom_id=f"{self.amount}")
        self.amount += 1
        return button

    def x(self):
        button = Button(label="X", custom_id=f"{self.x_amount}_x", style=ButtonStyle.red, disabled=True)
        self.x_amount += 1
        return button

    def o(self):
        button = Button(label="O", custom_id=f"{self.o_amount}_o", style=ButtonStyle.green, disabled=True)
        self.o_amount += 1
        return button


'''

            current_os = 0
            for j in range(3):
                for m in range(3):
                    if self.grid[j][m] == 0:
                        current_os += 1
            thing = self.valid(current_os)
            if thing is True:
                self.yes_msg = True

            if thing is False:
                self.yes_msg = "tie"

            if thing == "not":
                self.yes_msg = False



                    if self.yes_msg is False:
                        msg = self.update()
                    elif self.yes_msg is True:
                        msg = self.main_msg
                        if self.winning_letter == "X":
                            msg += f"{self.player2.mention}"
                        elif self.winning_letter == "O":
                            msg += f"{self.player1.mention}"
                    elif self.yes_msg == "tie":
                        msg = self.main_msg
                        msg += f"**it's a tie!**"
'''
