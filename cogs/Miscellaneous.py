import random

from discord.ext import commands
from discord.ext.commands import parameter

from functions import getCurrentDateTime, to_lower, to_upper


class Miscellaneous(commands.Cog, name='Miscellaneous Commands', description='Miscellaneous Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Gives the current date and time
    @commands.command(name='date', description='Gives the current date and time.\n---------------\n/date')
    async def _date_(self, ctx):
        await ctx.send(f'Today\'s date is {getCurrentDateTime()}.')

    # To lowercase
    @commands.command(name='low', description='Changes the input provided to lowercase.\n---------------\n/low <input>')
    async def _low_(self, ctx, *, input: to_lower = parameter(description='- Any input given by the user to be changed to lowercase')):
        await ctx.send(input)

    # To uppercase
    @commands.command(name='up', description='Changes the input provided to uppercase.\n---------------\n/up <input>')
    async def _up_(self, ctx, *, input: to_upper = parameter(description='- Any input given by the user to be changed to uppercase')):
        await ctx.send(input)

    # Wordcount of args
    @commands.command(name='count', description='Counts the amount of input given.\n---------------\n/count <input>')
    async def _count_(self, ctx, *, input: str = parameter(description='- Any amount of input given by the user to be counted')):
        await ctx.send(f'Count: {len(input)}')

    # Number calculations, returns float
    @commands.command(name='calc', description='Performs basic math calculations.\n---------------\n/calc <method> <first_number> <second_number>')
    async def _calc_(self, ctx, method: str = parameter(description='- Options are: [a | s | m | d]'), first_number: float = parameter(description='- First value used for calculations'), second_number: float = parameter(description='- Second value used for calculations')):
        if method == 'a':
            await ctx.send(f'{first_number}+{second_number} = {first_number + second_number}')
        elif method == 's':
            await ctx.send(f'{first_number}-{second_number} = {first_number - second_number}')
        elif method == 'm':
            await ctx.send(f'{first_number}*{second_number} = {first_number * second_number}')
        elif method == 'd':
            await ctx.send(f'{first_number}/{second_number} = {first_number / second_number}')
        else:
            await ctx.send(f'Unexpected expression after calc, try again {ctx.author.mention}', delete_after=5)

    # Random range based on two arguments
    @commands.command(name='range', description='Random number based on range given.\n---------------\n/range <bottom_of_range> <top_of_range>')
    async def _randomrange_(self, ctx, bottom_of_range: int = parameter(description='- Bottom of range for random value'), top_of_range: int = parameter(description='- Top of range for random value')):
        if bottom_of_range >= 0 and top_of_range >= 0:
            await ctx.send(f'From {bottom_of_range} to {top_of_range} your random number is: {random.randint(bottom_of_range, top_of_range)}')
        else:
            await ctx.send(f'{ctx.author.mention}, negative value detected. Try again...', delete_after=5)


async def setup(ChetBot):
    await ChetBot.add_cog(Miscellaneous(ChetBot))
