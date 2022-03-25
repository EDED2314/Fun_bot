import discord
from discord.ext import commands
from discord_components import ActionRow, Button, ButtonStyle, DiscordComponents
import asyncio

# noinspection PyTypeChecker
class PrivateVC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test_channel = 848238227583926277
        self.ctxx = None
        self.author = None
        self.respond = None
        self.pvc_list = []
        self.real_people = []
        self.number = 0
        self.true = True
        self.current_channel = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            pass
            # channel = member.guild.get_channel(self.test_channel)
            #  channel.send(f"{member.nick} joined {after.channel.name}")
        if before.channel is not None and after.channel is None:
            # channel = member.guild.get_channel(self.test_channel)
            pvc_role = member.guild.get_role(909228794815066152)
            try:
                await member.remove_roles(pvc_role)
            except:
                pass
            # await channel.send(f"{member.nick} left {before.channel.name}")
            for pvc in self.pvc_list:
                if pvc.name == before.channel.name:
                    await before.channel.delete()

    @staticmethod
    async def buttons(number: int):
        return Button(label=f"{number}", style=ButtonStyle.grey, custom_id=str(number))

    @commands.command()
    async def pvc(self, ctx):
        self.current_channel = ctx.channel
        await ctx.message.delete()
        self.ctxx = ctx
        embed = discord.Embed(title="**Choose the amount of people!**", colour=discord.Colour.dark_gray())
        components = [
            ActionRow(await self.buttons(1), await self.buttons(2), await self.buttons(3), await self.buttons(4))]
        await ctx.send(embed=embed, components=components)
        await asyncio.sleep(100)
        pvc_role = ctx.guild.get_role(909228794815066152)
        try:
            await ctx.author.remove_roles(pvc_role)
            for person in self.real_people:
                await person.remove_roles(pvc_role)
        except:
            pass
        self.real_people = []

    @commands.Cog.listener()
    async def on_button_click(self, i):
        if i.message.channel == self.current_channel:
            for k in range(1, 5):
                if i.component.custom_id == str(k):
                    if i.author != self.ctxx.author:
                        await i.respond(content="Hey buddy, thats not yours")
                    else:
                        await i.respond(content="Type a name you would want to give it in the chat")
                        self.author = i.author
                        self.respond = int(k)
                        await i.message.delete()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return
        try:
            if msg.author == self.author:
                self.number += 1
                if self.respond > 1:
                    if self.true:
                        await msg.reply("Please list out the names with @-ing", delete_after=10)
                        self.true = False
                    if "<@!" in msg.content:
                        people = msg.content.split()
                        for i in range(len(people)):
                            people[i] = str(people[i]).strip(">").strip("<").strip("@").strip("!")
                            self.real_people.append(msg.guild.get_member(int(people[i])))
                        for person in self.real_people:
                            pvc_role = msg.guild.get_role(909228794815066152)
                            await person.add_roles(pvc_role)

                if self.number >= 2:
                    self.author = None
                    self.true = True
                    self.number = 0
                    return
                else:
                    name = msg.content
                    pvcs = discord.utils.get(self.ctxx.guild.roles, name="pvc")

                    vc_cat = discord.utils.get(self.ctxx.guild.categories, id=848238227583926281)
                    pvc = await vc_cat.create_voice_channel(name=name)
                    self.pvc_list.append(pvc)

                    people = discord.utils.get(self.ctxx.guild.roles, id=848238731768234034)
                    await pvc.set_permissions(people, view_channel=False)

                    mods = discord.utils.get(self.ctxx.guild.roles, id=848242774868099103)
                    await pvc.set_permissions(mods, view_channel=True)

                    bots = discord.utils.get(self.ctxx.guild.roles, id=848246926155448350)
                    await pvc.set_permissions(bots, view_channel=True)

                    await msg.author.add_roles(pvcs)
                    await pvc.set_permissions(pvcs, view_channel=True)
                    await msg.delete()
                    await asyncio.sleep(100)
                    await pvc.delete()

        except AttributeError:
            return

