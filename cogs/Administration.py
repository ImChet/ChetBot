import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, parameter


class Administration(commands.Cog, name='Administration', description='Administration'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Kick command
    @commands.command(name='kick', hidden=True, description='Kicks users with optional specified reason.\n---------------\n/kick <member> <reason>')
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def _kick_(self, ctx, member: discord.Member = parameter(description='- The member you wish you kick'), *, reason: str = parameter(default=None, description='- The optional reason you kicked the user specified by <member>')):
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.', delete_after=5)

    # Ban command
    @commands.command(name='ban', hidden=True, description='Bans users with optional specified reason.\n---------------\n/ban <member> <reason>')
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def _ban_(self, ctx, member: discord.Member = parameter(description='- The member you wish you ban'), *, reason: str = parameter(default=None, description='- The optional reason you banned the user specified by <member>')):
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been banned.', delete_after=5)

    # Delete previous text command
    @commands.command(name='clear', hidden=True, description='Clears a specified backlog of messages in channel where command was invoked.\n(Limited to 100 previous clears)\n---------------\n/clear <amount>')
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def _delete_(self, ctx, amount: int = parameter(default=1, description='- Number of previous messages to clear')):
        if 0 < amount <= 100:
            async with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=amount)
                await ctx.send(f'Deleted {len(deleted):,} messages.', delete_after=5)
        else:
            await ctx.send(f'The amount provided is not within the allowed bounds. The allowable range is 1 to 100.')


async def setup(ChetBot):
    await ChetBot.add_cog(Administration(ChetBot))
