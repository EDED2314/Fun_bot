import itertools

'''
import discord
from discord.ext import commands, tasks
from discord_components import DiscordComponents
from dotenv import load_dotenv
import os
import glob

from cog_info import Info
from cog_teacher import Lee
from cog_pvc import PrivateVC
from cog_math import Math
from cog_wordle import Wordle
# from cog_music import Music

load_dotenv()

# ----------------------------------------------------
intents = discord.Intents.default()
intents.members = True
prefix = 'f.'
bot = commands.Bot(command_prefix=prefix, description="Fun bot made by Eddie :)", intents=intents)
bot.remove_command('help')

status = itertools.cycle([f'{prefix}help', 'with your mom', f'{prefix}help'])


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.event
async def on_ready():
    change_status.start()
    print(f"{bot.user.name} is ready")
    DiscordComponents(bot)


# ----------------------------------------------------
@bot.command()
async def shutdown(ctx):
    if ctx.author.id == 742015954967593101:
        shutdown_embed = discord.Embed(title='Bot Update',
                                       description='I am now shutting down. See you later. BYE! :slight_smile:',
                                       color=0x8ee6dd)
        await ctx.channel.send(embed=shutdown_embed)
        await bot.logout()
    else:
        shutdown_embed = discord.Embed(title='Bot Update',
                                       description='I am **not** now shutting down. See you *not** later. :slight_smile:',
                                       color=0x8ee6dd)
        await ctx.channel.send(embed=shutdown_embed)

@bot.command()
async def u(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)
# ----------------------------------------------------

if __name__ == '__main__':
    bot.add_cog(PrivateVC(bot))
    bot.add_cog(Info(bot))
    bot.add_cog(Math(bot))
    bot.add_cog(Lee(bot))
    bot.add_cog(Wordle(bot))
    # bot.add_cog(Music(bot))
    bot.run(os.getenv("TOKEN"), bot=bot)
'''
from dotenv import load_dotenv
import os
load_dotenv()

from bot import FunBot
from bot import PrivateVC
from bot import Math
from bot import Lee
from bot import TicTacToe
from bot import Wordle
from bot import Info
from bot import Counting
from bot import image_handler
from bot import Scrapper

bot = FunBot()
if __name__ == '__main__':
    bot.add_cog(PrivateVC(bot))
    bot.add_cog(Info(bot))
    bot.add_cog(Math(bot))
    bot.add_cog(Lee(bot))
    bot.add_cog(Wordle(bot))
    # bot.add_cog(Music(bot))
    bot.add_cog(Counting(bot))
    # bot.add_cog(TicTacToe(bot))
    bot.add_cog(Scrapper(bot))
    bot.add_cog(image_handler(bot))
    bot.run(os.getenv("TOKEN"), bot=bot)
