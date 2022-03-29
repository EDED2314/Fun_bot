from disnake.ext import commands
import disnake
import csv
import matplotlib.pyplot as plt
import pandas as pd


class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fieldnames = ["member", "errors"]
        self.num = 0
        self.current_channel_number = 0
        self.current_channel_list = 1
        self.do_not_do = False
        self.lines = None
        self.current_server = None
        self.current_channel = None

    def update(self):
        self.num = 0
        self.current_channel_number = 0
        self.current_channel_list = 1
        self.do_not_do = False

    async def sending(self, ctx, message=" "):
        embed = disnake.Embed(title=f"**Who-messed-up-in-counting logger**{message}", description="Please enter below which channel is your counting channel")
        text_channels = []
        text_channels_1 = []
        text_channels_2 = []
        text_channels_3 = []
        text_channels_4 = []
        text_channels_5 = []
        text_channels_6 = []
        text_channels_7 = []
        text_channels_8 = []
        text_channels_9 = []
        text_channels_10 = []
        text_channels_11 = []

        for channel in ctx.guild.text_channels:
            # print(channel.name)
            self.current_channel_number += 1
            if self.current_channel_number == 23:
                self.current_channel_list += 1

            if self.current_channel_list == 1:
                text_channels_1.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 2:
                text_channels_2.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 3:
                text_channels_3.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 4:
                text_channels_4.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 5:
                text_channels_5.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 6:
                text_channels_6.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 7:
                text_channels_7.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 8:
                text_channels_8.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 9:
                text_channels_9.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 10:
                text_channels_10.append(self.convert_to_selectoption(channel))
            elif self.current_channel_list == 11:
                text_channels_11.append(self.convert_to_selectoption(channel))

        text_channels.append(text_channels_1)
        text_channels.append(text_channels_2)
        text_channels.append(text_channels_3)
        text_channels.append(text_channels_4)
        text_channels.append(text_channels_5)
        text_channels.append(text_channels_6)
        text_channels.append(text_channels_7)
        text_channels.append(text_channels_8)
        text_channels.append(text_channels_9)
        text_channels.append(text_channels_10)
        text_channels.append(text_channels_11)

        componentss = []

        for i in range(self.current_channel_list):
            components = [
                disnake.ui.Select(
                    placeholder="Select the according counting channel!",
                    options=text_channels[i]
                    , custom_id=f"Select_{self.num}")
            ]
            componentss.append(components)
        self.num += 1

        await ctx.send(embed=embed)

        for item in componentss:
            await ctx.send(components=item)

        interaction = await self.bot.wait_for(
            "select_option"
        )
        channel = disnake.utils.get(ctx.guild.text_channels, id=int(interaction.values[0]))
        await interaction.edit_origin(content=f"{channel.name} selected!")

        return [channel, interaction]

    @commands.has_permissions(kick_members=True)
    @commands.command(name="counting_setup")
    async def counting_setup(self, ctx):
        x = await self.sending(ctx)
        interaction = x[1]
        self.update()

        # set up csv file and channel_id in txt ffile

        f = open(f'Counting_logs/{ctx.guild.name}.csv', 'w+')
        f.close()

        await self.write_counting_channels(interaction, ctx, "add")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def log_first_bits(self, ctx):
        with open(f"txt_files/counting_channels.txt", "r") as f:
            f.seek(0)
            lines = f.readlines()
            for item in lines:
                item = str(item)
                item = item.split("&&&&&&&&")
                self.current_server = item[0]
                self.current_channel = disnake.utils.get(ctx.guild.text_channels, id=int(item[1]))
                print(self.current_channel)
                done = False
                if self.current_channel is not None:
                    messages = await self.current_channel.history(limit=1000).flatten()
                    for i in range(len(messages)):
                        if "RUINED IT AT" in messages[i].content:
                            person_error_msg = messages[i + 1]
                            person = person_error_msg.author
                            if await self.check_if_member(person.name, ctx):
                                await self.add_error(person.name, ctx)
                            else:
                                await self.add_member(person.name, ctx)
                                await self.add_error(person.name, ctx)
                    done = True
                if done:
                    break
        await ctx.send("Done!")

    @commands.has_permissions(kick_members=True)
    @commands.command(name="change_counting")
    async def change_counting_channel(self, ctx):
        x = await self.sending(ctx, message="*changing*")
        interaction = x[1]
        self.update()

        await self.write_counting_channels(interaction, ctx, "remove")

    async def write_counting_channels(self, interaction, ctx, mode):
        with open(f"txt_files/counting_channels.txt", "r") as ff:
            ff.seek(0)
            lines = ff.readlines()
            # print(lines)
            for item in lines:
                item = str(item)
                item = item.split("&&&&&&&&")
                # print(item[0])
                if item[0] == ctx.guild.name:
                    self.do_not_do = True
            if mode == "add":
                if self.do_not_do:
                    await ctx.send(
                        f"Current server already setup! Use {self.bot.prefix}change_counting to change counting channel")
                else:
                    lines.append(f"{ctx.guild.name}&&&&&&&&{interaction.values[0]}\n")
                self.lines = lines

            if mode == "remove":
                copy_lines = []
                if self.do_not_do:
                    for item in lines:
                        item1 = str(item)
                        item1 = item1.split("&&&&&&&&")
                        # print(item[0])
                        if item1[0] != ctx.guild.name:
                            copy_lines.append(str(item))
                    copy_lines.append(f"{ctx.guild.name}&&&&&&&&{interaction.values[0]}\n")
                    # print(copy_lines)
                else:
                    await ctx.send(
                        f"Current server not setup! Use {self.bot.prefix}counting_setup to setup counting channel")
                self.lines = copy_lines

        with open(f"txt_files/counting_channels.txt", "w") as f:
            f.writelines(self.lines)

    @staticmethod
    def convert_to_selectoption(channel: disnake.TextChannel):
        label = channel.name
        value = channel.id
        return disnake.SelectOption(label=label, value=str(value))

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author == self.bot.user:
            return
        try:
            with open(f"txt_files/counting_channels.txt", "r") as f:
                f.seek(0)
                lines = f.readlines()
                for item in lines:
                    item = str(item)
                    item = item.split("&&&&&&&&")
                    self.current_server = item[0]
                    self.current_channel = disnake.utils.get(message.guild.text_channels, id=int(item[1]))
                    if message.channel == self.current_channel:
                        if message.author.id == 510016054391734273 and "RUINED IT AT" in message.content:
                            messages = await message.channel.history(limit=3).flatten()
                            print(messages)
                            for i in range(len(messages)):
                                if message.content in messages[i].content:
                                    person_error_msg = messages[i + 1]
                                    person = person_error_msg.author
                                    if await self.check_if_member(person.name, message):
                                        await self.add_error(person.name, message)
                                    else:
                                        await self.add_member(person.name, message)
                                        await self.add_error(person.name, message)
        except FileNotFoundError:
            await message.channel.send(
                f"To log **who** did it (this time it was {person.mention} that ruined it), do {self.bot.prefix}counting_setup!")

    async def add_error(self, member, message):
        rows = []
        r = csv.DictReader(open(f"Counting_logs/{message.guild.name}.csv", "r"))
        for row in r:
            if row['member'] == str(member):
                row['errors'] = int(row['errors']) + 1
            rows.append(row)
        w = csv.DictWriter(open(f"Counting_logs/{message.guild.name}.csv", 'w', newline=''), fieldnames=self.fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)
        return

    async def add_member(self, member, message):
        r = csv.DictReader(open(f"Counting_logs/{message.guild.name}.csv", "r"))
        rows = [row for row in r]
        rows.append({'member': member, 'errors': 0})
        w = csv.DictWriter(open(f"Counting_logs/{message.guild.name}.csv", 'w', newline=''), fieldnames=self.fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)
        return

    async def check_if_member(self, member, message):
        r = csv.DictReader(open(f"Counting_logs/{message.guild.name}.csv", "r"))
        for row in r:
            if row['member'] == str(member):
                return True
        return False

    async def plot(self, ctx):
        fig, ax = plt.subplots()
        data = pd.read_csv(f"Counting_logs/{ctx.guild.name}.csv")
        ax.bar(data["member"], data["errors"], width=0.5, edgecolor="black", linewidth=0.7)
        plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
        plt.savefig('errors_for_counting.png')
        embed = disnake.Embed(title="**People who got it wrong**")
        await ctx.send(embed=embed, file=disnake.File('errors_for_counting.png'))

    @commands.command(name="plot")
    async def plotting_errors(self, ctx):
        await self.plot(ctx)
