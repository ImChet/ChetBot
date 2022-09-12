import asyncio
import os
import discord
from discord.ext import commands


class FileOperations(commands.Cog, name='File Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Makes and uploads files bases on user's decision
    @commands.command(name='file')
    async def _makeFile_(self, ctx, fileType, *args):
        await ctx.typing()

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
        if ctx.message.attachments:

            await ctx.typing()

            # Check if file type of the attachment matched the declared initial value
            initial_check = f'/{initial}'
            jpg_check = ['/jpeg', '/jpg']
            check_counter = 0
            file_increment = 1
            limit = len(ctx.message.attachments)

            # .jpeg and .jpg is the same
            if initial_check in jpg_check:
                initial_check = '/jpeg'

            # Checks if the initial declared value matched actual uploaded attachment file type
            for in_progress in range(0, limit + 1):
                working_attachment = str(ctx.message.attachments[in_progress].content_type)
                if initial_check in working_attachment:
                    type_check = initial_check in working_attachment
                    print(ctx.message.attachments[in_progress].content_type)  # Testing
                    check_counter = check_counter + 1
                elif initial_check not in working_attachment:
                    await ctx.send(
                        f'{ctx.author.mention}, the initial file type you declared doesn\'t match the file type of the attachment.', delete_after=5)
                    break

                if check_counter == limit:
                    break

            # Ensures the FilesToConvert directory exists
            path = 'WorkingFiles/FilesToConvert/'
            directory_exists = os.path.exists(path)
            if directory_exists is False:
                os.mkdir(path)

            if type_check:
                for attachment in ctx.message.attachments:
                    # Download the user attachments on iterator through list
                    await attachment.save(f'WorkingFiles/FilesToConvert/{attachment.filename}')

                    # Converter logic goes here
                    to_convert = f'WorkingFiles/FilesToConvert/{attachment.filename}'

                    # Set output type as desired
                    output_filepath = f'WorkingFiles/FilesToConvert/ChetBot_Converted_{file_increment}.{desired}'
                    # Save(output_filepath)

                    await ctx.send(f'{ctx.author.mention}, here is your converted file from .{initial} to .{desired}:')
                    await ctx.send(file=to_convert)
                    # await ctx.send(file=output_filepath)

                    # Increment file names by 1 to keep filenames unique
                    file_increment = file_increment+1

        else:
            await ctx.send(f'{ctx.author.mention}, no attachments were found to convert.', delete_after=5)

        # Must sleep (10s) to prevent errors
        await asyncio.sleep(10)
        # After output is sent, delete WorkingFiles/FilesToConvert/*
        working_directory = 'WorkingFiles/FilesToConvert'
        for file in os.scandir(working_directory):
            os.remove(file.path)
            print(f'I removed {file.name}')  # Testing

    @_convert_.error
    async def _convert_error(self, ctx, error):
        if isinstance(error, discord.HTTPException):
            await ctx.send(f'{ctx.author.mention}, saving your attachment failed.', delete_after=5)
        elif isinstance(error, discord.NotFound):
            await ctx.send(f'{ctx.author.mention}, no attachments were found to convert.', delete_after=5)


async def setup(ChetBot):
    await ChetBot.add_cog(FileOperations(ChetBot))
