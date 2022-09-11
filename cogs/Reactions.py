import discord
from discord.ext import commands


class Reactions(commands.Cog, name='Reaction Listener'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Reaction add listener
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member: discord.Member):
        channel = reaction.message.channel
        # await reaction.message.reply(f'{member.name} added {reaction.emoji}')

    # Reaction remove listener
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, member: discord.Member):
        channel = reaction.message.channel
        # await reaction.message.reply(f'{member.name} removed {reaction.emoji}')


async def setup(ChetBot):
    await ChetBot.add_cog(Reactions(ChetBot))
