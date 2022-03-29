import disnake
from typing import List
from disnake.ext import commands

import typing


class MyView(disnake.ui.View):
    message: disnake.Message

    def __init__(self):
        super().__init__(timeout=30.0)

    async def on_timeout(self):
        # Once the view times out we disable the first button and remove the second button
        self.children[0].disabled = True  # type: ignore
        self.remove_item(self.children[1])
        # make sure to update the message with the new buttons
        await self.message.edit(view=self)

    @disnake.ui.button(label="Click to disable the view", style=disnake.ButtonStyle.red)
    async def disable(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):

        # We disable every single component in this view
        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        # make sure to update the message with the new buttons
        await interaction.response.edit_message(view=self)

        # Prevents on_timeout from being triggered after the buttons are disabled
        self.stop()

    @disnake.ui.button(label="Click to remove the view", style=disnake.ButtonStyle.red)
    async def remove(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        # view = None removes the view
        await interaction.response.edit_message(view=None)

        # Prevents on_timeout from being triggered after the view is removed
        self.stop()

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        """Starts a tic-tac-toe game with yourself."""
        view = MyView()

        # Sends a message with the view
        view.message = await ctx.send("These buttons will be disabled or removed", view=view)
