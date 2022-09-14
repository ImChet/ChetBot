from discord.ext import commands

from functions import getCurrentDateTime


class OnReady(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # on_ready is called when the Bot has logged on/set things up
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.ChetBot.user} on {getCurrentDateTime()}')

async def setup(ChetBot):
    await ChetBot.add_cog(OnReady(ChetBot))
