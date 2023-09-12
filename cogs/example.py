import discord
from discord.ext import commands
# a basic set up of how cogs work
class example(commands.Cog):#that means it inherits from command.cog
    def __init__(self,client):
        self.client=client

    #for events
    @commands.Cog.listener()#function decorator within a cog --> takes place of @client.event
    async def on_ready(self):
        #usually does not take args but bc its in a class takes self
        print("Bot is online")

    @commands.command()#for commands
    async def ping(self,ctx):
        await ctx.send("pong")

async def setup(client):
    await client.add_cog(example(client))