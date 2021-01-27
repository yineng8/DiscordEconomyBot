import discord
import asyncio
import os
import random
import json

from discord.ext import commands

from dotenv import load_dotenv

# eventually change to read from cogs directory
extensions = [
    'cogs.help',
    'cogs.bank',
    'cogs.admin',
    'cogs.owners',
    'cogs.casino',
    'cogs.shop',
] 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


# honestly does this even do anything?
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


for ext in extensions:
    bot.load_extension(ext)

bot.run(TOKEN)
