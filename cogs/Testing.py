import discord
from discord import app_commands
from discord.ext import commands


class Testing(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    @commands.hybrid_command(name='test', with_app_command=True, description='Testing...')
    # remove this when syncing globally
    # avoid ratelimiting
    # guild=discord.Object(id=495623660967690240)
    @app_commands.guilds(495623660967690240)
    async def test(self, ctx: commands.Context) -> None:
        # ephemeral=True makes it so that only the user that invoked can see the response
        await ctx.send(f'This is the test command', ephemeral=True)


async def setup(ChetBot: commands.Bot) -> None:
    await ChetBot.add_cog(Testing(ChetBot))
