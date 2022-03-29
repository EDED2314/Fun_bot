from disnake.ext import commands
import disnake
import Scrappers


class Scrapper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.amount = 30

    @commands.command(name='wiki')
    async def wiki_search(self, ctx, *kwargs: str):
        wiki = Scrappers.Wikipedia()
        if kwargs[0].startswith("https"):
            result = await wiki.get_page(kwargs[0])
            '''
            for idx, val in enumerate(result):
                await ctx.send(val)
                if idx >= self.amount - 1:
                    break
            '''
            try:
                result[1]
            except IndexError:
                await ctx.send(result[0])
                return

            await ctx.send(content=f"{result[0]}\n{result[1]}\n{ctx.author.mention} **Your wikipedia article as a txt file!**", file=disnake.File("Scrappers/txts/wikipedia.txt", "Article.txt"))
        else:
            url = "https://en.wikipedia.org/wiki/example"
            if len(kwargs) == 1:
                url = f"https://en.wikipedia.org/wiki/{kwargs[0]}"
            if len(kwargs) == 2:
                url = f"https://en.wikipedia.org/wiki/{kwargs[0]}_{kwargs[1]}"
            if len(kwargs) == 3:
                url = f"https://en.wikipedia.org/wiki/{kwargs[0]}_{kwargs[1]}_{kwargs[2]}"
            if len(kwargs) == 4:
                url = f"https://en.wikipedia.org/wiki/{kwargs[0]}_{kwargs[1]}_{kwargs[2]}_{kwargs[3]}"

            result = await wiki.get_page(url)

            # print(len(result[0]))
            '''
            for idx, val in enumerate(result):
                await ctx.send(val)
                if idx >= self.amount - 1:
                    break
            '''
            try:
                result[1]
            except IndexError:
                await ctx.send(result[0])
                return

            await ctx.send(content=f"{result[0]}\n{result[1]}\n{ctx.author.mention} **Your wikipedia article as a txt file!**", file=disnake.File("Scrappers/txts/wikipedia.txt", "Article.txt"))


            # await ctx.send(result)
