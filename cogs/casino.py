#casino commands
import discord
import asyncio
import os
import random
from discord.ext import commands

#fucking letter emojis for future use
emojiletter = [
    '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲',
    '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿',
]

class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='roulette', help='Simulates a roulette')
    async def rlt(self, ctx):
        msg = await ctx.send("not yet implemented")

        for em in emojiletter:
            await msg.add_reaction(em)

    @commands.command(name='coinflip', help='Simulates flipping a coin.', aliases=['cf'])
    async def cflip(self, ctx):

        side = ["heads", "tails"]
        coin = [
            str(random.choice(side))
        ]
        await ctx.send(', '.join(coin))

    @commands.command(name='rolldice', help='Simulates rolling dice.')
    async def roll(self, ctx):

        dice = [
            str(random.choice(range(1, 6)))

        ]
        await ctx.send(', '.join(dice))



def setup(bot):
    bot.add_cog(Casino(bot))