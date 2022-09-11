import random
from discord.ext import commands
from functions import getDateTime, to_lower, to_upper


class Simple(commands.Cog, name='Simple Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Gives the current date and time
    @commands.command()
    async def date(self, ctx):
        await ctx.send(f'Today\'s date is {getDateTime()}.')

    # To lowercase
    @commands.command()
    async def low(self, ctx, *, content: to_lower):
        await ctx.send(content)

    # To uppercase
    @commands.command()
    async def up(self, ctx, *, content: to_upper):
        await ctx.send(content)

    # Example of using an unknown amount of variable arguments
    # Wordcount of args
    @commands.command()
    async def wordcount(self, ctx, *args):
        await ctx.send(f'The text provided has {len(args)} words.')

    # Number calculations, returns float
    @commands.command(name='calc')
    async def _calc_(self, ctx, fn, a: float, b: float):
        if fn == 'a':
            await ctx.send(f'{a}+{b} = {a + b}')
        elif fn == 's':
            await ctx.send(f'{a}-{b} = {a - b}')
        elif fn == 'm':
            await ctx.send(f'{a}*{b} = {a * b}')
        elif fn == 'd':
            await ctx.send(f'{a}/{b} = {a / b}')
        else:
            await ctx.send(f'Unexpected expression after calc, try again {ctx.author.mention}')

    # Random range based on two arguments
    @commands.command(name='rr')
    async def _randomrange_(self, ctx, a: int, b: int):
        await ctx.send(f'From {a} to {b} your random number is: {random.randint(a, b + 1)}')


async def setup(ChetBot):
    await ChetBot.add_cog(Simple(ChetBot))