import discord
from discord.ext import commands

# a simple cog with a button
class button(discord.ui.View):
    def __init__(self,*,timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="clickme",style=discord.ButtonStyle.gray)
    async def click(self,interaction:discord.Interaction , button:discord.ui.Button):
        await interaction.response.send_message("You clicked me")


class Button(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog Loaded")

    @commands.command()
    async def click(self,ctx):
       await ctx.send("Message with a button",view =button())


async def setup(client):
    await client.add_cog(Button(client))
