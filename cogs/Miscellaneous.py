import random

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import parameter

from functions import getCurrentDateTime, to_lower, to_upper


class Miscellaneous(commands.Cog, name='Miscellaneous Commands', description='Miscellaneous Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Gives the current date and time
    @commands.hybrid_command(name='date', with_app_command=True, description='Gives the current date and time.')
    async def _date_(self, ctx: commands.Context) -> None:
        await ctx.send(f'Today\'s date is {getCurrentDateTime()}.')

    # To lowercase
    @commands.hybrid_command(name='low', with_app_command=True, description='Changes the input provided to lowercase.')
    @app_commands.describe(user_input='Any input given by the user to be changed to lowercase')
    async def _low_(self, ctx: commands.Context, *, user_input: to_lower = parameter(description='- Any input given by the user to be changed to lowercase')) -> None:
        await ctx.send(user_input)

    # To uppercase
    @commands.hybrid_command(name='up', with_app_command=True, description='Changes the input provided to uppercase.')
    @app_commands.describe(user_input='Any input given by the user to be changed to uppercase')
    async def _up_(self, ctx: commands.Context, *, user_input: to_upper = parameter(description='- Any input given by the user to be changed to uppercase')) -> None:
        await ctx.send(user_input)

    # Wordcount of args
    @commands.hybrid_command(name='count', with_app_command=True, description='Counts the amount of input given.')
    @app_commands.describe(user_input='Any amount of input given by the user to be counted')
    async def _count_(self, ctx: commands.Context, *, user_input: str = parameter(description='- Any amount of input given by the user to be counted')) -> None:
        await ctx.send(f'Count: {len(user_input)}')

    # Random range based on two arguments
    @commands.hybrid_command(name='range', with_app_command=True, description='Random number based on range given.')
    @app_commands.describe(bottom_of_range='Bottom of range for random value', top_of_range='Top of range for random value')
    async def _randomrange_(self, ctx: commands.Context, bottom_of_range: int = parameter(description='- Bottom of range for random value'), top_of_range: int = parameter(description='- Top of range for random value')) -> None:
        if bottom_of_range >= 0 and top_of_range >= 0:
            await ctx.send(f'From {bottom_of_range} to {top_of_range} your random number is: {random.randint(bottom_of_range, top_of_range)}')
        else:
            await ctx.send(f'{ctx.author.mention}, negative value detected. Try again...', delete_after=5)

    # Defining the 'calc' hybrid group command
    @commands.hybrid_group(name='calc', with_app_command=True, description='Performs basic math calculations.\n/calc <method> <first_number> <second_number>')
    async def _calc_(self, ctx: commands.Context) -> None:
        print('I am the calc voice command')

    @_calc_.command(name='a', with_app_command=True, description='Addition')
    @app_commands.describe(first_number='First number you wish to use in your simple calculations',
                           second_number='Second number you wish to use in your simple calculations')
    async def _addition_(self, ctx: commands.Context, first_number: float, second_number: float) -> None:
        await ctx.send(f'{first_number}+{second_number} = {first_number + second_number}')

    @_calc_.command(name='s', with_app_command=True, description='Subtraction')
    @app_commands.describe(first_number='First number you wish to use in your simple calculations',
                           second_number='Second number you wish to use in your simple calculations')
    async def _subtraction_(self, ctx: commands.Context, first_number: float, second_number: float) -> None:
        await ctx.send(f'{first_number}-{second_number} = {first_number - second_number}')

    @_calc_.command(name='m', with_app_command=True, description='Multiplication')
    @app_commands.describe(first_number='First number you wish to use in your simple calculations',
                           second_number='Second number you wish to use in your simple calculations')
    async def _multiplication_(self, ctx: commands.Context, first_number: float, second_number: float) -> None:
        await ctx.send(f'{first_number}*{second_number} = {first_number * second_number}')

    @_calc_.command(name='d', with_app_command=True, description='Division')
    @app_commands.describe(first_number='First number you wish to use in your simple calculations',
                           second_number='Second number you wish to use in your simple calculations')
    async def _division_(self, ctx: commands.Context, first_number: float, second_number: float) -> None:
        await ctx.send(f'{first_number}/{second_number} = {first_number / second_number}')


async def setup(ChetBot):
    await ChetBot.add_cog(Miscellaneous(ChetBot))
