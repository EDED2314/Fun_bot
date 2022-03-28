import glob, os
import discord
from discord.ext import commands
import random
import requests

class Lee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.direct = r"daniel_pics/"

    @commands.command()
    async def lee(self, ctx, mode="pic"):
        self.oldpwd = os.getcwd()
        if mode == "pic":
            x = random.choice(self.check_numbers(mode="list"))
            await ctx.send(file=discord.File(f'daniel_pics/lee{x}.png'))
        if mode == "test":
            await ctx.send("30%")
    '''
    @commands.command(name="post")
    async def upload_lee_file(self, ctx, mode="lee"):
        attachment_url = ctx.message.attachments[0].url
        file_request = requests.get(attachment_url)
        # await ctx.send(attachment_url)
        os.chdir(self.oldpwd)
        large_num = None
        if mode == "lee":
            open("temp_im.png", 'wb').write(file_request.content)
            large_num = self.check_numbers('temp_im.png')
        if mode == "flug":
            open("temp_im.png", 'wb').write(file_request.content)
            large_num = self.check_numbers('temp_im.png', folder="flug_pics")
        if large_num is None:
            await ctx.send(embed=discord.Embed(title="**Please Upload Another Image! Image Already In Storage!**"))
        else:
            if mode == "lee":
                open(f'daniel_pics/lee{large_num + 1}.png', 'wb').write(file_request.content)
            elif mode == "flug":
                open(f'{mode}_pics/flug{large_num + 1}.png', 'wb').write(file_request.content)
            embed = discord.Embed(title=f"**sucessfully saved image as a {mode} image!**")
            embed.set_image(url=attachment_url)
            await ctx.send(embed=embed)
    '''
    def check_numbers(self, image=None, mode="greatest", folder="daniel_pics"):
        os.chdir(f"{folder}")
        lst = []
        old_num = len(glob.glob("*.png"))
        for file in glob.glob("*.png"):
            file_name = str(file)
            file_name = file_name.strip(".")
            file_name = file_name.strip("png")
            if folder == "daniel_pics":
                file_name = file_name.strip("lee")
                file_name = file_name.strip(".")
            elif folder == "flug_pics":
                file_name = file_name.strip("flug")
                file_name = file_name.strip(".")
            lst.append(int(file_name))
            # check if image rpeats
            if image is not None:
                if open(f"Fun_bot/{image}", "rb").read() == open(file,
                                                                 "rb").read():
                    return None

        os.chdir(self.oldpwd)
        if mode == "greatest":
            return old_num
        elif mode == "list":
            return lst

    @commands.command()
    async def flug(self, ctx, mode="pic"):
        self.oldpwd = os.getcwd()
        if mode == "pic":
            x = random.choice(self.check_numbers(mode="list", folder="flug_pics"))
            await ctx.send(file=discord.File(f'flug_pics/flug{x}.png'))

# ----------------------------------------------------