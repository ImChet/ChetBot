import discord
from discord.ext import commands


class FileOperations(commands.Cog, name='File Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Makes and uploads files bases on user's decision
    @commands.command(name='file')
    async def _makeFile_(self, ctx, fileType, *args):
        # .typing() makes it look like ChetBot is typing
        async with ctx.channel.typing():
            if fileType == 'csv':
                userArgs = ','.join(args)
                f = open("WorkingFiles/ChetBot.csv", "w")
                f.write(userArgs)
                f.close()
                myfile = discord.File('WorkingFiles/ChetBot.csv')
                await ctx.send(f'{ctx.author.mention} here is the file that you wanted me to create:\n')
                await ctx.send(file=myfile)
            elif fileType == 'tab':
                userArgs = '\t'.join(args)
                f = open("WorkingFiles/ChetBot.csv", "w")
                f.write(userArgs)
                f.close()
                myfile = discord.File('WorkingFiles/ChetBot.csv')
                await ctx.send(f'{ctx.author.mention} here is the file that you wanted me to create:\n')
                await ctx.send(file=myfile)
            elif fileType == 'n':
                userArgs = '\n'.join(args)
                f = open("WorkingFiles/ChetBot.csv", "w")
                f.write(userArgs)
                f.close()
                myfile = discord.File('WorkingFiles/ChetBot.csv')
                await ctx.send(f'{ctx.author.mention} here is the file that you wanted me to create:\n')
                await ctx.send(file=myfile)
            else:
                await ctx.send(f'Unexpected argument.\nThe options for this command are \"csv\", \"tab\", and \"n\".\n')


async def setup(ChetBot):
    await ChetBot.add_cog(FileOperations(ChetBot))
