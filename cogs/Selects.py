import discord
from discord.ext import commands


class Selects(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot


async def setup(ChetBot):
    await ChetBot.add_cog(Selects(ChetBot))
