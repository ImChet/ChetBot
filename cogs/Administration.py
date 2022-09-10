import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class Administration(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Kick command
    @commands.command(name='kick')
    @has_permissions(kick_members=True)
    async def _kick_(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.')

    # Ban command
    @commands.command(name='ban')
    @has_permissions(ban_members=True)
    async def _ban_(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been banned.')


async def setup(ChetBot):
    await ChetBot.add_cog(Administration(ChetBot))
