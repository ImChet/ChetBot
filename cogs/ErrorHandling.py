from discord.ext import commands


class ErrorHandling(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Error catch
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, you don\'t have permission to run this command.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'{ctx.author.mention}, your inputted arguments are invalid.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, the command you chose requires arguments that are missing.')


async def setup(ChetBot):
    await ChetBot.add_cog(ErrorHandling(ChetBot))
