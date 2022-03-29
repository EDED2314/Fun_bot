import disnake
from disnake.ext import commands
import random
import textwrap

# noinspection PyUnresolvedReferences
class WordleGame():
    def __init__(self):
        word = self.get_word()
        self.word = word.upper()
        self.base = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]
                     ]

        print(self.word)

        self.string1 = " "
        self.current_word = ""
        self.wordle_message = None
        self.yellow_letters = []
        self.green_letters = []
        self.used_letters = []

    @staticmethod
    def get_word():
        with open("txt_files/words.txt", "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip("\n")
            randomint = random.randint(0, 5000)
            randomint1 = random.randint(0, 5000)
            randomint2 = random.randint(0, 5756)
            randomnum = randomint // randomint1 + randomint2
            return lines[randomnum]

    async def display_grid(self, word: str, row: int):
        if len(word) != 5:
            raise ConnectionError
        for i in range(len(word)):
            self.base[row][i] = word[i].upper()
            # print(self.base)

        word_list = []
        for letter in self.word:
            letter = f"{letter}"
            word_list.append(letter)

        duplicate_base_row = self.base[row]
        for i in range(len(duplicate_base_row)):
            duplicate_base_row[i] = f"{str(duplicate_base_row[i]).replace('*', '')}"

        new_word_list = []
        new_duplicate_base_row = []

        for i in range(5):
            if word_list[i] != duplicate_base_row[i]:
                new_word_list.append(word_list[i])
                new_duplicate_base_row.append(duplicate_base_row[i])

        yellow_letters = []

        for i in range(len(new_word_list)):
            for k in range(len(new_duplicate_base_row)):
                if new_word_list[i] == new_duplicate_base_row[k]:
                    yellow_letters.append(new_word_list[i])

        print(word_list)
        print(self.base[row])
        print(yellow_letters)
        # format
        for letter in yellow_letters:
            index = self.base[row].index(letter)
            self.base[row][index] = f"__{self.base[row][index]}__"

        # check if it is letter
        green_letters = []
        for i in range(len(word)):
            letterr = f"{str(self.base[row][i]).strip('_')}"
            if letterr == self.word[i]:
                self.base[row][i] = f"**{self.word[i]}**"
                green_letters.append(self.base[row][i])

        used_letters = []
        for letter in self.base[row]:
            if not letter.startswith("_") and not letter.startswith("*"):
                used_letters.append(letter)

        self.yellow_letters = yellow_letters
        self.used_letters = used_letters
        self.green_letters = green_letters

        word_list = []
        for letter in self.word:
            letter = f"**{letter}**"
            word_list.append(letter)

        maybe_return = False

        for i in range(len(word)):
            if self.base[row] == word_list:
                # this means they got it, they won
                maybe_return = True

        duplicate = self.base
        for i in range(len(duplicate)):
            for k in range(len(duplicate)):
                if duplicate[i][k] == 0:
                    duplicate[i][k] = "-"

        for i in range(len(duplicate)):
            for k in range(len(duplicate)):
                if k == 4:
                    self.string1 += f" {str(duplicate[i][k])} \n"
                else:
                    self.string1 += f" {str(duplicate[i][k])} "

        string = self.string1
        self.string1 = " "
        if maybe_return:
            return string, "win"
        return string

    async def play(self, bot: commands.Bot, ctx: commands.context.Context):
        embed = await self.start_embed(ctx)
        await ctx.send(embed=embed)
        tries = 5
        for num in range(5):
            self.current_word = await bot.wait_for('message', check=lambda message: message.author == ctx.author,
                                                   timeout=600)
            self.current_word = self.current_word.content
            await self.check_word(ctx)
            grid = await self.display_grid(self.current_word, num)
            if type(grid) is not str:
                embed = await self.wordle_embed(grid[0], ctx)
                self.wordle_message = await ctx.send(embed=embed)
                return f"{ctx.author.mention} **Congrats**, You *Won*! 🥳"
            else:
                embed = await self.wordle_embed(grid, ctx)
                tries -= 1
                self.wordle_message = await ctx.send(embed=embed)
        if tries == 0:
            return f"😭 {ctx.author.mention} **YoU SuCk** The word was *{self.word}* 😒"

    async def wordle_embed(self, grid: str, ctx):
        embed = disnake.Embed(title=f"**{ctx.author.name}'s Wordle Game!**", color=disnake.Colour.random(),
                              description=grid)
        embed.set_footer(text="Use `f.wordle rules` to see the hints")
        correct_string = "|"
        incorrect_string = "|"
        not_in_place = "|"
        for item in self.green_letters:
            correct_string += f"{item}|"
        for item in self.yellow_letters:
            not_in_place += f"{item}|"
        for item in self.used_letters:
            incorrect_string += f"{item}|"
        embed.add_field(name="Correct Letters", value=correct_string)
        embed.add_field(name="Not in place Letters", value=not_in_place)
        embed.add_field(name="Incorrect Letters", value=incorrect_string)
        return embed

    async def check_word(self, ctx):
        if len(self.current_word) != 5:
            m = await ctx.send(f"{ctx.author.mention} 😒 bro send a 5 letter word")
            await m.reply(content="Remeber to do f.wordle to play again!")
            return "lost"

    @staticmethod
    async def start_embed(ctx: commands.context.Context):
        embed = disnake.Embed(title=f"**{ctx.author.name}'s Wordle Game!**", color=disnake.Colour.random(),
                              description="Type a 5 letter word to begin!")
        embed.set_footer(text="Use `f.wordle rules` to see the hints")
        return embed


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed():
        prefix = "f."
        embed = disnake.Embed(title="**Eddie's Wordle Game Help Panel**")
        description = textwrap.dedent(f"""
        `{prefix}wordle` help - help panel
        `{prefix}wordle` rules - sends the rules and instructions on how to play
        `{prefix}wordle` 
        `{prefix}wordle`
        """)
        embed.description = description
        return embed

    @staticmethod
    async def rules_embed():
        embed = disnake.Embed(title="**Eddie's Wordle Game Rules Panel**")
        description = textwrap.dedent(f"""
        > Letter  means that it is **not in the word**
        > **Letter**  means that it is in the word and **in** the correct place
        > __Letter__ means that it is the word but **not** in the correct place
        """)
        embed.description = description
        return embed

    @commands.command(name="wordle")
    async def wordle(self, ctx, mode="new"):
        if mode == "new":
            wordle_game = WordleGame()
            msg = await wordle_game.play(self.bot, ctx)
            await ctx.send(msg)
        if mode == "rules":
            embed = await self.rules_embed()
            await ctx.send(embed=embed)
        if mode == "help":
            embed = await self.help_embed()
            await ctx.send(embed=embed)