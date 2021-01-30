import discord
import asyncio
import os
import random
import json
from discord.ext import commands




class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    


    @commands.command(name='shop', help='Lists items in shop.')
    async def shop(self, ctx):
        mainshop = [{"name":"Watch","price":100,"description":"Time"},
                    {"name":"Laptop","price":1000,"description":"Work"},
                    {"name":"Car","price":10000,"description":"Drive"},
                    {"name":"House","price":100000,"description":"Live"},
                    {"name":"Boat","price":1000000,"description":"Sail"},
                    {"name":"Plane","price":10000000,"description":"Fly"}]


        em = discord.Embed(title = "Shop")

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = name, value = f"${price} | {desc}")

        shop_display = await ctx.send (embed = em)

        
        await shop_display.add_reaction("⌚")
        await shop_display.add_reaction("💻")
        await shop_display.add_reaction("🚗")
        await shop_display.add_reaction("🏠")
        await shop_display.add_reaction("🛥️")
        await shop_display.add_reaction("🛩️")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['⌚', '💻', '🚗', '🏠', '🛥️', '🛩️']


        try:

            reaction, self.user = await self.bot.wait_for('reaction_add', timeout=30, check=check)

            if reaction.emoji == '⌚':

                await self.buy(ctx, "watch", amount = 1)

            elif reaction.emoji == '💻':
                await self.buy(ctx, "laptop", amount = 1)

            elif reaction.emoji == '🚗':
                await self.buy(ctx, "car", amount = 1)

            elif reaction.emoji == '🏠':
                await self.buy(ctx, "house", amount = 1)
            
            elif reaction.emoji == '🛥️':
                await self.buy(ctx, "boat", amount = 1)
            
            elif reaction.emoji == '🛩️':
                await self.buy(ctx, "plane", amount = 1)


        except asyncio.TimeoutError:
            await ctx.send("Timed out")






    @commands.command(name='buy', help='buy (item) (amount)')
    async def buy(self, ctx, item, amount = 1):
        await self.open_account(ctx.author)
        res = await self.buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have enough money in your wallet")
                return
        await ctx.send(f"you just bought {amount} {item}")

    

    @commands.command(name='bag', help='Check bag.')
    async def bag(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_bank_data()
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []
        em= discord.Embed(title="Bag")
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            em.add_field(name = name, value= amount)
        await ctx.send(embed = em)
    
    
    
    
    
    
    async def buy_this(self, user, item_name, amount):
        mainshop = [{"name":"Watch","price":100,"description":"Time"},
                    {"name":"Laptop","price":1000,"description":"Work"},
                    {"name":"Car","price":10000,"description":"Drive"},
                    {"name":"House","price":100000,"description":"Live"},
                    {"name":"Boat","price":1000000,"description":"Sail"},
                    {"name":"Plane","price":10000000,"description":"Fly"}]

        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break
        if name_ == None:
            return [False,1]
        cost = price*amount
        users = await self.get_bank_data()
        bal = await self.update_bank(user)

        if bal[0]<cost:
            return [False,2]
        try:
            index=0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1 
                    break
                if t == None:
                    obj = {"item":item_name,"amount" : amount}
                    users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item":item_name,"amount" : amount}
            users[str(user.id)]["bag"] = [obj]
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        await self.update_bank(user,cost*-1,"wallet")
        return [True,"worked"]


    
    
    
    
    
    
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
    bot.add_cog(Shop(bot))
    # references class
