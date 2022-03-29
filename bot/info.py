import disnake
from disnake.ext import commands
import textwrap
import asyncio
import random
import datetime

class Info(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        prefix = 'f.'
        description = textwrap.dedent(f"""
        **Fun Stuff**
        `{prefix}help` - this help command
        `{prefix}pvc` - private vc with interface
        `{prefix}u` [user by @ing them] - userinfo 
        `{prefix}wordle` - wordle
        **Teachers**
        `{prefix}lee` - lee picture 😳
        `{prefix}lee test` - shows ur test grade from Mr.Lee
        `{prefix}flug` - flug picture 😳
        **Math** 
        `{prefix}math` [mode]
        **Counting**
        `{prefix}counting_setup` - sets up the channel to log people who make erros in counting
        `{prefix}change_counting` - changes the channel to log people
        `{prefix}plot` - plots who got the errors lol
        `{prefix}log_first_bits` - logs first bits of data
        **Photos**
        `{prefix}photopanel` - a gui to blur and sharpen images 📷
         **My stuff**
         `{prefix}shutdown` - a command only executable by the person himself - eddie
        """)
        self.embed = disnake.Embed(title="**Help**", description=description, colour=disnake.Colour.random())
        self.b = 1
        self.message = None
        self.embed = disnake.Embed(title="**Nothing to snipe （＞人＜；）**")

    @commands.command(name="help")
    async def helpp(self, ctx: commands.Context):
        embed = self.embed
        embed.set_footer(text=f"fun bot help § requested by {ctx.author.name}", icon_url=self.bot.user.avatar.url)
        m = await ctx.send(embed=embed)
        self.message = m.id
        await m.add_reaction("🚮")

    @commands.command(name="ping")
    @commands.has_permissions(kick_members=True)
    async def pinggg(self, ctx, use: disnake.User, times: int):
        await asyncio.sleep(0.2)
        await ctx.message.delete()
        await asyncio.sleep(0.2)
        b = 0
        while b < times:
            await ctx.send(f"{use.mention}")
            b += 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if f"<@!{self.bot.user.id}>" in message.content:
            embed = self.embed
            embed.set_footer(text=f"Fun-bot help § requested by {message.author.name}",
                             icon_url=self.bot.user.avatar.url)
            m = await message.channel.send(embed=embed)
            self.message = m.id
            await m.add_reaction("🚮")
        if "urmom" in message.content or "your mom" in message.content or "mum" in message.content:
            lst = ["😩I would eat *your mom* if I had to chance to", "deez nuts in **urmum** 😏",
                   "*yourmom* **is** indeed kinda sussy 📮", "sometimes, people have to chill on the yourmom jokes 😒"]
            await message.reply(random.choice(lst))

    @commands.Cog.listener()
    async def on_reaction_add(self, payload, user):
        if user == self.bot.user:
            return
        if str(payload) == "🚮" and payload.message.id == self.message:
            await payload.message.delete()

    @commands.command()
    async def shutdown(self, ctx):
        if ctx.author.id == 742015954967593101:
            shutdown_embed = disnake.Embed(title='Bot Update',
                                           description='I am now shutting down. See you later. BYE! :slight_smile:',
                                           color=0x8ee6dd)
            await ctx.channel.send(embed=shutdown_embed)
            await self.bot.logout()
        else:
            shutdown_embed = disnake.Embed(title='Bot Update',
                                           description='I am **not** now shutting down. See you *not** later. :slight_smile:',
                                           color=0x8ee6dd)
            await ctx.channel.send(embed=shutdown_embed)

    @commands.command()
    async def u(self, ctx, *, user: disnake.Member = None):
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = disnake.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = disnake.Embed(color=disnake.Colour.random())
        embed.set_author(name=f"{message.author} said:", icon_url=message.author.avatar.url)
        attachment = message.content
        try:
            for idx, val in enumerate(message.attachments):
                attachment += f"\n[Attachment{idx+1}]({val.url})"
            embed.set_image(message.attachments[0].url)
        except IndexError:
            pass
        embed.description = attachment
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        embed.set_footer(text=f"Today at {current_time}")
        self.embed = embed

    @commands.command()
    async def snipe(self, ctx):
        await ctx.send(embed=self.embed)


# ----------------------------------------------------