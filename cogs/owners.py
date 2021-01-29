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

    async def cog_check(self, ctx):
        if ctx.author.id in owners:
            return True

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))
        print(f'invalid id: {ctx.author.id}')
        await ctx.send("You cannot access this command.")

    @commands.command(name='reset', aliases=['r'])
    async def resetuser(self, ctx, member: discord.Member):
        await self.open_account(member)
        users = await self.get_bank_data()

        users[str(member.id)]["wallet"] = 0
        users[str(member.id)]["bank"] = 0
        users.pop("bag", None)
        
        with open("mainbank.json", "w") as f:
            json.dump(users, f)

        await ctx.send(f"You reset {member}")

    @resetuser.error
    async def resetuser_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please @ a user")

    @commands.command(name='resetall', aliases=['rall'])
    async def resetall(self, ctx):
        
        await self.open_account(ctx.author)
        users = await self.get_bank_data()
        for user in users.values():
            user['wallet'] = 0
            user['bank'] = 0
            user.pop("bag", None)
        
        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    @commands.command(name='generate', help='me only', aliases=['gen'])
    async def generatemoney(self, ctx, amount, member: discord.Member = None):
        if member == None:
            await self.open_account(ctx.author)
            users = await self.get_bank_data()
            user = ctx.author
        else:
            await self.open_account(member)
            users = await self.get_bank_data()
            user = member

        earnings = int(amount)

        await ctx.send(f"You got {earnings}")

        users[str(user.id)]["wallet"] += earnings
        users[str(user.id)]["bank"] += earnings

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