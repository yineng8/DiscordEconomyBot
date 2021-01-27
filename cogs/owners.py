# file for owner-specific commands
# need to be manually added in order to use
import discord
import asyncio
import os
import random
import json
from discord.ext import commands

owners = {160881596579184640, 230820515097477120}

class Owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def isowner(self, isid):
        for id in owners:
            if isid == id:
                return True
        return False

    @commands.command(name='generate', help='me only', aliases=['gen'])
    async def generatemoney(self, ctx, amount):
        if not ctx.author.id in owners:
            print(ctx.author.id)
            return
        
        await self.open_account(ctx.author)

        users = await self.get_bank_data()

        user = ctx.author

        earnings = int(amount)

        await ctx.send(f"You got {earnings}")

        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users, f)



    async def open_account(self, user):

        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0

        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        return True

    async def get_bank_data(self):
        with open("mainbank.json", "r") as f:
            users = json.load(f)
        return users

    async def update_bank(self, user, change=0, mode="wallet"):
        users = await self.get_bank_data()

        users[str(user.id)][mode] += change

        with open("mainbank.json", "w") as f:
            json.dump(users, f)

        bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
        return bal

def setup(bot):
    bot.add_cog(Owners(bot))