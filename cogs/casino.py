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

        flag = True

        em = discord.Embed(title = "CoinFlip")
        shop_display = await ctx.send (embed = em)

        await shop_display.add_reaction("🇭")
        await shop_display.add_reaction("🇹")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['🇭', '🇹']


        try:

            reaction, self.user = await self.bot.wait_for('reaction_add', timeout=30, check=check)

            if reaction.emoji == '🇭':
                flag = True

            elif reaction.emoji == '🇹':
                flag = False


            side = ["heads", "tails"]
            coin = [
                str(random.choice(side))
            ]
            
            
            if (coin == ['heads']) and (flag == True):
                await ctx.send('you win')
            

            elif (coin == ['tails']) and (flag == False):
                await ctx.send('you win')
            
            else:
                await ctx.send('you lose')

        except asyncio.TimeoutError:
            await ctx.send("Timed out")




    @commands.command(name='rolldice', help='Simulates rolling dice.')
    async def roll(self, ctx):

        dice = [
            str(random.choice(range(1, 6)))

        ]
        await ctx.send(', '.join(dice))



def setup(bot):
    bot.add_cog(Casino(bot))