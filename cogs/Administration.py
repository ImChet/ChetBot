import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions
from typing import Optional


class Administration(commands.Cog, name='Administration Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Kick command
    @commands.command(name='kick', hidden=True)
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def _kick_(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.', delete_after=5)

    # Ban command
    @commands.command(name='ban', hidden=True)
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def _ban_(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been banned.', delete_after=5)

    # Delete previous text command
    @commands.command(name='clear', hidden=False)
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def _delete_(self, ctx, amount: Optional[int] = 1):
        if 0 < amount <= 100:
            # .typing() makes it look like ChetBot is typing
            async with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=amount)
                await ctx.send(f'Deleted {len(deleted):,} messages.', delete_after=5)
        else:
            await ctx.send(f'The amount provided is not within the allowed bounds. The allowable range is 1 to 100.')


async def setup(ChetBot):
    await ChetBot.add_cog(Administration(ChetBot))
