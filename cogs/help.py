################################
# for now it is unused
# will be updated with a better
# help menu
################################
from discord.ext import commands

class Helpdesk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Helpdesk(bot))