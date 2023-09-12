import asyncio
import os

import discord
from discord.ext import commands, tasks


intents = discord.Intents.default()
#intents.messages_content = True

client = commands.Bot(intents= discord.Intents.all(),command_prefix=".")




#loads and unloads commands
@client.command()
async def load(ctx,extension):#extension is the cog that will be loaded
    client.load_extension("cogs."+extension)

@client.command()
async def unload(ctx,extension):#extension is the cog that will be loaded
    client.unload_extension("cogs."+extension)


async def main():
    #loads all the cog files
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            await client.load_extension("cogs."+filename[:-3])

asyncio.run(main())


client.run("token")