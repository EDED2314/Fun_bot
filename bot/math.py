import disnake
from disnake.ext import commands
import textwrap
import math

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.b = 1
        self.prefix = "f."
        self.description = textwrap.dedent(f"""
            `{self.prefix}math gcd` - finds greatest common divisor between the numbers 
            `{self.prefix}math growth`- compound intrest calculator 
            `{self.prefix}math permute` - permutations 
            `{self.prefix}math`
            """)
        self.compound = False
        self.n = 1
        self.chosing_and_permutations = ChoosingAndPermutations()

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, OverflowError):
         await ctx.send("😒 bruh send something smaller")
        elif isinstance(error, commands.MissingRequiredArgument):
            description = self.description
            embed = disnake.Embed(title="**Math commands panel**📝", description=description)
            await ctx.send(embed=embed)
        else:
            await ctx.send('An error occurred: {}'.format(str(error)))


    @commands.command(name="math")
    async def math(self, ctx, mode):
        if mode == "gcd" or mode == "gcf":
            lst = await self.double_input_embed(ctx, self.bot, "gcd")
            number1, number2 = lst[0], lst[1]
            await self.greatest_common_divisor(ctx, number1, number2)

        if mode == "permute":
            lst = await self.double_input_embed(ctx, self.bot, "permute")
            n, r = lst[0], lst[1]
            if float(n) > 100 or float(r) > 100:
                raise OverflowError
            try:
                number = self.chosing_and_permutations.permutate(n, r)
                await ctx.send(embed=disnake.Embed(title=f"**The permutation of the two numbers is {number:,.2f}**".format(number=number)))
            except TypeError:
                await ctx.send("**The calculator right now only supports integer values for permutations/combinations, sorry!**")

        if mode == "growth":
            try:
                got_nums = await self.growth_embed(ctx, self.bot)
                if self.compound:
                    self.n = got_nums[4]
                try:
                    result = got_nums[0] * ((1 + got_nums[2] / self.n) ** (self.n * got_nums[1]))
                    author = ctx.author.name
                    await ctx.send(embed=disnake.Embed(
                        title=f"**{author}'s results with these numbers: {result:,.2f}.**".format(result=result,
                                                                                                  author=ctx.author.name),
                        description=got_nums[3]))
                    self.n = 1
                except OverflowError:
                    await ctx.send(f"{ctx.author.mention} bruh enter smaller numbers 😒")
                    self.n = 1
                    raise ConnectionError
            except ConnectionError:
                await ctx.send("Please redo `f.math growth` because you entered n, or mistyped")
        if mode == "vector":
            calc = MatrixAndVectorCalc()
        if mode == "matrixes":
            return

        return

    async def growth_embed(self, ctx, bot):
        # string = "formula is A = P(1+r/n)^nt"
        description = "Please enter numbers as following:" \
                      "[Starting price] [time yrs] [rate %] (compound)"
        embed = disnake.Embed(title="**Compound Intrest Calculator**", description=description)
        await ctx.send(embed=embed)
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author,
                                 timeout=600)
        msg_content = msg.content.split()
        self.compound = False
        try:
            nums_got = textwrap.dedent(f"""
            > Starting Price: {msg_content[0]}
            > Time: {msg_content[1]} yrs
            > Rate: {msg_content[2]} %
            > Compound: {msg_content[3]}
            """)
            self.compound = True
        except IndexError:
            nums_got = textwrap.dedent(f"""
            > Starting Price: {msg_content[0]} 
            > Time: {msg_content[1]} yrs
            > Rate: {msg_content[2]} %
            > Compound: Annually (once a year)
            """)
        embed = disnake.Embed(title="Alright I have these numbers is it correct? (y/n):", description=nums_got)
        await ctx.send(embed=embed)
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author,
                                 timeout=600)
        y_or_n = str(msg.content.upper())
        for i in range(len(msg_content)):
            try:
                if msg_content[i].upper() == "E":
                    msg_content[i] = math.e
                msg_content[i] = float(msg_content[i])
            except ValueError:
                raise ConnectionError
        if "Y" in y_or_n:
            if self.compound:
                return [msg_content[0], msg_content[1], msg_content[2] / 100, nums_got, msg_content[3]]
            else:
                return [msg_content[0], msg_content[1], msg_content[2] / 100, nums_got]
        else:
            raise ConnectionError

    @staticmethod
    async def double_input_embed(ctx, bot, mode):
        if mode == "gcd":
            embed = disnake.Embed(title="**Greatest common factor/divsor calculator**",
                                  description="Please enter number 1 and number 2 below like such: num1 num2")
            await ctx.send(embed=embed)
        if mode == "permute":
            embed = disnake.Embed(title="**Permutation Calculator**",
                                  description="Please enter n and r below like such: n r")
            await ctx.send(embed=embed)
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author,
                                 timeout=600)
        msg = msg.content
        msg = msg.split()
        print(msg)
        msg[0] = float(msg[0])
        msg[1] = float(msg[0])


        return msg

    async def greatest_common_divisor(self, ctx, number1, number2):
        try:
            nums = (int(number1), int(number2))
        except ValueError:
            await ctx.send(embed=disnake.Embed(title="**Enter a number please!**"))
            return

        gcd = await self.e_form(nums[0], nums[1])
        await ctx.send(embed=disnake.Embed(title=f"**The gcd of the two numbers is {gcd}**"))

    async def e_form(self, num1: int, num2: int):
        maxn = max(num1, num2)
        minn = min(num1, num2)
        if maxn == minn:
            return maxn
        else:
            return await self.e_form(maxn - minn, minn)


class ChoosingAndPermutations:

    def permutate(self, n: float, r: float):
        # nPr=n!/(n-r)!
        fact_n = self.factorial(n)
        fact_n_r = self.factorial((n - r))
        print(fact_n)
        return fact_n/fact_n_r

    '''    def choosing(self, n: float, r: float):
        # nCr=n!/(n-r)!r!
        fact_n = self.factorial(n)
        fact_n_r = self.factorial((n - r))
        fact_r = self.factorial(r)
        print(fact_n, fact_r)
        return fact_n / (fact_n_r*fact_r)'''


    def factorial(self, urnum):
        urnum = int(urnum)
        fact = 1
        for i in range(1, urnum + 1):
            fact = fact * i
        return fact


class Scaler:
    def __init__(self, num: float):
        self.value = num


class Matrix2x2:
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.matrix_rows = [Vector(a, b), Vector(c, d)]
        self.matrix_cols = [Vector(a, c), Vector(b, d)]
        self.matrix = [[self.a, self.b], [self.c, self.d]]

    def refresh(self):
        self.matrix_rows = [Vector(self.a, self.b), Vector(self.c, self.d)]
        self.matrix_cols = [Vector(self.a, self.c), Vector(self.b, self.d)]

    def inverse(self):
        determinant = self.a * self.d - self.c * self.b
        if determinant == 0:
            return "uninvertable"
        x = 1 / determinant
        scaler = Scaler(x)
        inverse = self * scaler
        return inverse

    def __mul__(self, other):
        # returns a vector!!
        if isinstance(other, Vector):
            x = self.matrix_rows[0] * other
            y = self.matrix_rows[1] * other
            return Vector(x, y)
        if isinstance(other, Matrix2x2):
            col1 = self * other.matrix_cols[0]
            col2 = self * other.matrix_cols[1]
            return Matrix2x2(col1.x, col2.x, col1.y, col2.y)
        if isinstance(other, Scaler):
            self.a = self.a * other.value
            self.b = self.b * other.value
            self.c = self.c * other.value
            self.d = self.d * other.value
            self.refresh()

    def __sub__(self, other):
        if isinstance(other, Matrix2x2):
            return Matrix2x2(self.a - other.a, self.b - other.b, self.c - other.c, self.a - other.c)

    def __add__(self, other):
        if isinstance(other, Matrix2x2):
            return Matrix2x2(self.a + other.a, self.b + other.b, self.c + other.c, self.a + other.c)


class Vector:
    def __init__(self, v1: float, v2: float):
        self.x = v1
        self.y = v2

    @property
    def mag(self):
        x = self.x ** 2
        y = self.y ** 2
        m = x + y
        return math.sqrt(m)

    def __add__(self, other):
        if isinstance(other, Vector):
            numx = self.x + other.x
            numy = self.y + other.y
            return Vector(numx, numy)

    def __sub__(self, other):
        if isinstance(other, Vector):
            numx = self.x - other.x
            numy = self.y - other.y
            return Vector(numx, numy)

    def __mul__(self, other):
        if isinstance(other, Vector):
            result = self.x * other.x + self.y * other.y
            return result
        if isinstance(other, Scaler):
            self.x = self.x * other.value
            self.y = self.x * other.value
        if isinstance(other, Matrix2x2):
            x = other.matrix_rows[0] * self
            y = other.matrix_rows[1] * self
            return Vector(x, y)


class MatrixAndVectorCalc:
    def __init__(self):
        return

    @staticmethod
    def area_of_parallel(v1: Vector, v2: Vector):
        var = v1.x * v2.y - v1.y * v2.x
        return math.fabs(var)

    @staticmethod
    def find_invert_vector_with_matrix(matrix: Matrix2x2, vector: Vector):
        # e.g. A^-1(1;3)
        a = matrix.a
        b = matrix.b
        c = matrix.c
        d = matrix.d
        x = vector.x
        y = vector.y
        v2 = (a * y - c * x) / (a * d - c * b)
        v1 = (x - b * v2) / a
        return Vector(v1, v2)

    @staticmethod
    def find_invert_matrix_2x2_with_2_vector(v_1: Vector, v_2: Vector, v_3: Vector, v_4: Vector):
        # e.g. find a where a^-1(3;1) = (4;1) and a^-1(4;3) = (6;9)
        v1 = v_1.x
        v2 = v_1.y
        v3 = v_2.x
        v4 = v_2.y
        v5 = v_3.x
        v6 = v_3.y
        v7 = v_4.x
        v8 = v_4.y
        b = (v3 * v5 - v7 * v1) / (v3 * v8 - v7 * v4)
        a = (v1 - b * v4) / v3
        d = (v3 * v6 - v7 * v2) / (v3 * v8 - v7 * v4)
        c = (v2 - d * v4) / v3
        return Matrix2x2(a, b, c, d)

    @staticmethod
    def find_matrix_2x2_with_2_vector(v_1: Vector, v_2: Vector, v_3: Vector, v_4: Vector):
        v1 = v_2.x
        v2 = v_2.y
        v3 = v_1.x
        v4 = v_1.y
        v5 = v_4.x
        v6 = v_4.y
        v7 = v_3.x
        v8 = v_3.y
        b = (v3 * v5 - v7 * v1) / (v3 * v8 - v7 * v4)
        a = (v1 - b * v4) / v3
        d = (v3 * v6 - v7 * v2) / (v3 * v8 - v7 * v4)
        c = (v2 - d * v4) / v3
        return Matrix2x2(a, b, c, d)
