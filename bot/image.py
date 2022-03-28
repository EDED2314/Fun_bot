import discord
from discord.ext import commands, tasks
from small_photo_editor import SharpenerBlur
from discord_components import Button, ActionRow, ButtonStyle


# noinspection PyTypeChecker
class image_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.kernel_size = 3
        self.magnitude = 1
        self.sharpener = SharpenerBlur
        self.ctx = None
        self.bluring_kernel_size = 1
        self.number_kernel = 3
        self.number_mag = 1

    @commands.command(name="photopanel")
    async def photo_panel(self, ctx):
        self.ctx = ctx
        link = None
        components = self.make_components()
        image_types = ["png", "jpeg", "gif", "jpg"]
        for attachment in ctx.message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save("small_photo_editor/before_edit_img.png")
            link = attachment.url

        try:
            x = ctx.message.attachments[0]
        except IndexError:
            await ctx.send("Attach an Image Please! :C")
            return
        await ctx.message.delete()
        embed = discord.Embed(title=f"{ctx.author.name}'s **photo editing** session!")
        embed.set_image(url=link)
        m = await ctx.send(embed=embed,
                           components=components)
        self.m = m
        self._photopaneldisabler.start()


    @tasks.loop(seconds=30)
    async def _photopaneldisabler(self):
        pass

    @_photopaneldisabler.after_loop
    async def _photopaneldisablercatcher(self):
        try:
            await self.m.delete()
        except discord.errors.NotFound:
            return


    @commands.Cog.listener()
    async def on_button_click(self, i):
        if i.message.author == self.bot.user:
            if i.component.label == "<<":
                self.bluring_kernel_size += 3
                self.number_kernel -= 3
                self.number_mag -= 1

                if self.kernel_size > 3:
                    self.kernel_size -= 3
                elif self.magnitude != 1:
                    self.magnitude -= 1
                if self.number_kernel < 0 and self.number_mag < 0:
                    await self.sharpener.blur_ig(self.bluring_kernel_size)
                elif self.number_kernel >= 1:
                    await self.sharpener.sharpen_ig(self.kernel_size, self.magnitude)
                elif self.number_kernel < 0 and self.number_mag >= 0:
                    await self.sharpener.sharpen_ig(1, self.magnitude)
            if i.component.label == "<":
                self.bluring_kernel_size += 1
                self.number_kernel -= 1
                if self.kernel_size != 1:
                    self.kernel_size -= 1

                if self.number_kernel < 0 and self.number_mag < 0:
                    await self.sharpener.blur_ig(self.bluring_kernel_size)
                elif self.number_kernel >= 1:
                    await self.sharpener.sharpen_ig(self.kernel_size, self.magnitude)
                elif self.number_kernel < 0 and self.number_mag >= 0:
                    await self.sharpener.sharpen_ig(1, self.magnitude)

            if i.component.label == ">":
                self.kernel_size += 1
                self.number_kernel += 1

                if self.bluring_kernel_size != 1:
                    self.bluring_kernel_size -= 1
                await self.sharpener.sharpen_ig(self.kernel_size, self.magnitude)
            if i.component.label == ">>":
                if self.bluring_kernel_size > 3:
                    self.bluring_kernel_size -= 3
                self.magnitude += 1
                self.number_mag += 1
                await self.sharpener.sharpen_ig(self.kernel_size, self.magnitude)
            components = self.make_components()
            await i.respond(content="🎦 To **save** the image, right click it! 🎥", files=[discord.File("small_photo_editor/after_edit_img.png", filename="Image.png")],
                            components=components)
            try:
                self._photopaneldisabler.cancel()
                self._photopaneldisabler.start()
            except RuntimeError:
                return
    '''
    async def _sharpen(self, ctx, kernel_size: int, magnitude: int):
        image_types = ["png", "jpeg", "gif", "jpg"]
        for attachment in ctx.message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save("small_photo_editor/before_edit_img.png")

        try:
            x = ctx.message.attachments[0]
        except IndexError:
            await ctx.send("Attach an Image Please! :C")
            return

        sharpener = SharpenerBlur()
        await sharpener.sharpen_ig(kernel_size, magnitude)
        await ctx.send(file=discord.File("small_photo_editor/after_edit_img.png", filename="Image.png"))
    '''

    @staticmethod
    def make_components():
        big_left = Button(label="<<", custom_id="<<", style=ButtonStyle.blue)
        left = Button(label="<", custom_id="<", style=ButtonStyle.blue)
        right = Button(label=">", custom_id=">", style=ButtonStyle.blue)
        big_right = Button(label=">>", custom_id=">>", style=ButtonStyle.blue)

        row = [ActionRow(big_left, left, right, big_right)]
        return row

    @staticmethod
    def make_components_disabled():
        big_left = Button(label="<<", custom_id="<<", style=ButtonStyle.blue, disabled=True)
        left = Button(label="<", custom_id="<", style=ButtonStyle.blue, disabled=True)
        right = Button(label=">", custom_id=">", style=ButtonStyle.blue, disabled=True)
        big_right = Button(label=">>", custom_id=">>", style=ButtonStyle.blue, disabled=True)
        row = [ActionRow(big_left, left, right, big_right)]
        return row
