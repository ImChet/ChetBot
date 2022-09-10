import discord
from discord.ext import commands


class FileOperations(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Makes and uploads files bases on user's decision
    @commands.command(name='file')
    async def _makeFile_(self, ctx, name, *args):
        if name == 'csv':
            userArgs = ','.join(args)
            f = open("WorkingFiles/ChetBot.csv", "w")
            f.write(userArgs)
            f.close()
            myfile = discord.File('WorkingFiles/ChetBot.csv')
            await ctx.send(f'{ctx.author.mention} here is the comma seperated file that you wanted me to create:\n')
            await ctx.send(file=myfile)
        elif name == 'tab':
            userArgs = '\t'.join(args)
            f = open("WorkingFiles/ChetBot.csv", "w")
            f.write(userArgs)
            f.close()
            myfile = discord.File('WorkingFiles/ChetBot.csv')
            await ctx.send(f'{ctx.author.mention} here is the tab separated file that you wanted me to create:\n')
            await ctx.send(file=myfile)
        elif name == 'n':
            userArgs = '\n'.join(args)
            f = open("WorkingFiles/ChetBot.csv", "w")
            f.write(userArgs)
            f.close()
            myfile = discord.File('WorkingFiles/ChetBot.csv')
            await ctx.send(f'{ctx.author.mention} here is the new line separated file that you wanted me to create:\n')
            await ctx.send(file=myfile)
        else:
            await ctx.send(
                f'Unexpected expression after file, try again {ctx.author.mention}\nThe options for this command are \"csv\", \"tab\", and \"n\".\n')


async def setup(ChetBot):
    await ChetBot.add_cog(FileOperations(ChetBot))
