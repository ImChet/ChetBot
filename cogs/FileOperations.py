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

    # Coverts user attachments to desired type
    @commands.command(name='convert')
    async def _convert_(self, ctx, initial: str, desired: str):
        async with ctx.channel.typing():
            initial = f'/{initial}'
            desired = f'/{desired}'
            index = 0
            if ctx.message.attachments:
                limit = len(ctx.message.attachments)

                for x in range(index, limit+1):
                    working_attachment = str(ctx.message.attachments[x].content_type)

                    # .jpeg and .jpg is the same
                    if '/jpeg' or '/jpg' in initial:
                        initial = '/jpeg'

                    # Check if file type of the attachment matched the declared initial value
                    if initial in working_attachment:
                        print(ctx.message.attachments[x].content_type)  # Testing
                        await ctx.send(f'The attachment file type matches what you said')  # Testing

                        # Need to download the user attachments to WorkingFiles/FilesToConvert
                        # Attachment.save
                        # Converter logic goes here, use ConvertAPI
                        # Need to set input type as working_attachment
                        # Set output type as desired

                    else:
                        ctx.send(f'The initial file type you declared doesn\'t match the file type of the attachment.')
            else:
                await ctx.send(f'{ctx.author.mention}, no attachments were uploaded with your command.', delete_after=5)


async def setup(ChetBot):
    await ChetBot.add_cog(FileOperations(ChetBot))
