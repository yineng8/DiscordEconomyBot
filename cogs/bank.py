import discord
import asyncio
import os
import random
import json
from discord.ext import commands


class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='pay', help='Pay other player.')
    async def give(self, ctx, member: discord.Member, amount=None):
        await self.open_account(ctx.author)
        await self.open_account(member)

        amount = int(amount)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)

        if amount > bal[1]:
            await ctx.send("You don't have that much money")
            return

        if amount <= 0:
            await ctx.send("Amount must be positive")
            return

        await self.update_bank(ctx.author, -1*amount, "wallet")
        await self.update_bank(member, 1*amount, "wallet")

        emb = discord.Embed(
            description=f"You gave {member.name} {amount} bitcoins", color=0x2ecc71)
        await ctx.send(embed=emb)


    @commands.command(name='balance', help='Check user balance.', aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            await self.open_account(ctx.author)
            user = ctx.author
            users = await self.get_bank_data()

            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)].get("bank", 0)

            em = discord.Embed(
                title=f"{ctx.author.name}'s balance", color=discord.Color.red())
            em.add_field(name="Wallet Balance", value=wallet_amt)
            em.add_field(name="Bank Balance", value=bank_amt)
            await ctx.send(embed=em)
            return

        await self.open_account(member)
        user = member
        users = await self.get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)].get("bank", 0)

        em = discord.Embed(
            title=f"{member.name}'s balance", color=discord.Color.red())
        em.add_field(name="Wallet Balance", value=wallet_amt)
        em.add_field(name="Bank Balance", value=bank_amt)
        await ctx.send(embed=em)


    @commands.command(name='work', help='Go to work and get paid.')
    async def beg(self, ctx):
        await self.open_account(ctx.author)

        users = await self.get_bank_data()

        user = ctx.author

        earnings = random.randrange(345)

        await ctx.send(f"Someone gave you {earnings} coins!!")

        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users, f)


    @commands.command(name='withdraw', help='Withdraw money.')
    async def withdraw(self, ctx, amount=None):
        await self.open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive!")
            return

        await self.update_bank(ctx.author, amount)
        await self.update_bank(ctx.author, -1*amount, "bank")

        await ctx.send(f"you withdrew {amount} coins")

    @commands.command(name='deposit', help='Deposit money.')
    async def deposit(self, ctx, amount=None):
        await self.open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive!")
            return

        await self.update_bank(ctx.author, -1*amount)
        await self.update_bank(ctx.author, amount, "bank")

        await ctx.send(f"you deposit {amount} coins")

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
    bot.add_cog(Bank(bot))