import asyncio
import os

import discord
from discord.ext import commands
from pyffmpeg import FFmpeg
from PyPDF2 import PdfFileMerger

from functions import file_conversion


class FileOperations(commands.Cog, name='File Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Makes and uploads files bases on user's decision
    @commands.command(name='create')
    async def _create_file_(self, ctx, fileType, *args):
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
    @commands.command(name='file')
    async def _convert_files_(self, ctx, initial: str, desired: str):
        await ctx.typing()
        if ctx.message.attachments:

            print(str(ctx.message.attachments[0].content_type))  # Testing

            # Defining variables in use
            initial_check = f'/{initial}'
            allowed_files = ['/pdf', '/jpeg', '/jpg', '/docx', '/png']
            jpg_files = ['/jpeg', '/jpg']
            pdf_file = ['/pdf']
            docx_file = ['/docx']
            png_file = ['/png']
            check_counter = 0
            limit = len(ctx.message.attachments)

            # Conditional variable definitions
            supported_file_check = initial_check in allowed_files
            jpg_check = initial_check in jpg_files
            pdf_check = initial_check in pdf_file
            docx_check = initial_check in docx_file
            png_check = initial_check in png_file

            # Cleaning up user input
            if supported_file_check:
                if jpg_check:
                    initial_check = 'image/jpeg'  # .jpg/.jpeg
                elif pdf_check:
                    initial_check = 'application/pdf'  # .pdf
                elif docx_check:
                    initial_check = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # .docx
                elif png_check:
                    initial_check = 'image/png'  # .png
                else:
                    await ctx.send(f'{ctx.author.mention}, the type of file attached is not currently supported.',
                                   delete_after=10)
                # Checks if the initial declared value matched actual uploaded attachment file type
                for working_file in range(0, limit + 1):
                    working_file_attachment = str(ctx.message.attachments[working_file].content_type)
                    if initial_check in working_file_attachment:
                        type_check = initial_check in working_file_attachment
                        check_counter = check_counter + 1

                    elif initial_check not in working_file_attachment:
                        await ctx.send(
                            f'{ctx.author.mention}, the initial file type you declared doesn\'t match the file type of the attachment.',
                            delete_after=10)
                        break

                    if check_counter == limit:
                        break

                # Ensures the FilesToConvert directory exists
                path = 'WorkingFiles/FilesToConvert/'
                directory_exists = os.path.exists(path)
                if directory_exists is False:
                    os.mkdir(path)

                if type_check:
                    await ctx.send(f'{ctx.author.mention}, I am processing your request...', delete_after=3)
                    for attachment in ctx.message.attachments:
                        # Download the user attachments on iterator through list
                        await attachment.save(f'WorkingFiles/FilesToConvert/{attachment.filename}')
                        # Input file
                        input_filepath = f'WorkingFiles/FilesToConvert/{attachment.filename}'
                        # Output file
                        outfile = file_conversion(input_filepath, desired)
                        print(f'Sending converted file(s) now...')
                        if outfile is None:
                            await ctx.send(
                                f'{ctx.author.mention}, the file conversion you attempted is not currently supported.',
                                delete_after=10)
                            break
                        elif outfile is not None:
                            await ctx.send(file=discord.File(outfile))
                            print(f'File(s) successfully sent.')
            else:
                await ctx.send(
                    f'{ctx.author.mention}, the initial file type you declared doesn\'t match the file type of the attachment.',
                    delete_after=10)
        else:
            await ctx.send(f'{ctx.author.mention}, no attachments were found to convert.', delete_after=10)

        # Must sleep (20s) to prevent possible errors with the deletion of files
        await asyncio.sleep(20)
        # After output is sent, delete WorkingFiles/FilesToConvert/*
        working_directory = 'WorkingFiles/FilesToConvert'
        for file in os.scandir(working_directory):
            os.remove(file.path)

    @_convert_files_.error
    async def _convert_error(self, ctx, error):
        if isinstance(error, discord.HTTPException):
            await ctx.send(f'{ctx.author.mention}, saving your attachment failed.', delete_after=10)
        elif isinstance(error, discord.NotFound):
            await ctx.send(f'{ctx.author.mention}, no attachments were found to convert.', delete_after=10)

    # Coverts user audio attachments from allowed types
    @commands.command(name='audio')
    async def _convert_audio_(self, ctx, initial: str, desired: str):
        await ctx.typing()
        if ctx.message.attachments:

            # Defining variables in use
            initial_check = f'/{initial}'
            audio_types = ['/mp4', '/mp3', '/wav']
            mp4_file = ['/mp4']
            mp3_file = ['/mp3']
            wav_file = ['/wav']
            check_counter = 0
            limit = len(ctx.message.attachments)

            # Conditional variable definitions
            supported_audio_check = initial_check in audio_types
            mp4_check = initial_check in mp4_file
            mp3_check = initial_check in mp3_file
            wav_check = initial_check in wav_file

            # Content_types are either ['video/mp4', 'audio/mpeg', 'audio/x-wav'], cleaning up user input
            if supported_audio_check:
                if mp4_check:
                    initial_check = 'video/mp4'
                elif mp3_check:
                    initial_check = 'audio/mpeg'
                elif wav_check:
                    initial_check = 'audio/x-wav'
                else:
                    await ctx.send(f'{ctx.author.mention}, the type of file attached is not currently supported.',
                                   delete_after=10)

                # Checks if the initial declared value matched actual uploaded attachment file type
                for audio_file in range(0, limit + 1):
                    working_audio_attachment = str(ctx.message.attachments[audio_file].content_type)
                    if initial_check in working_audio_attachment:
                        type_check = initial_check in working_audio_attachment
                        check_counter = check_counter + 1
                    elif initial_check not in working_audio_attachment:
                        await ctx.send(
                            f'{ctx.author.mention}, the initial file type you declared doesn\'t match the file type of the attachment.',
                            delete_after=10)
                        break

                    if check_counter == limit:
                        break

                # Ensures the FilesToConvert directory exists
                path = 'WorkingFiles/FilesToConvert/'
                directory_exists = os.path.exists(path)
                if directory_exists is False:
                    os.mkdir(path)

                if type_check:
                    await ctx.send(f'{ctx.author.mention}, I am processing your request...', delete_after=3)
                    for attachment in ctx.message.attachments:
                        # Download the user attachments on iterator through list
                        await attachment.save(f'WorkingFiles/FilesToConvert/{attachment.filename}')
                        # Keeping the file name uploaded by the user without the previous unconverted extension
                        trimmed_filename = (os.path.splitext(str(attachment.filename))[0])
                        # Input file
                        input_filepath = f'WorkingFiles/FilesToConvert/{attachment.filename}'
                        # Output file
                        output_filepath = f'WorkingFiles/FilesToConvert/{trimmed_filename}.{desired}'
                        # Defining ff to FFmpeg
                        ff = FFmpeg()
                        # Setting the conversion as the downloaded user file, to the desired user file type
                        out_file = ff.convert(input_filepath, output_filepath)
                        await ctx.send(file=discord.File(out_file))
            else:
                await ctx.send(
                    f'{ctx.author.mention}, the initial file type you declared doesn\'t match the file type of the attachment.',
                    delete_after=10)
        else:
            await ctx.send(f'{ctx.author.mention}, no attachments were found to convert.', delete_after=10)

        # Must sleep (20s) to prevent possible errors with the deletion of files
        await asyncio.sleep(20)
        # After output is sent, delete WorkingFiles/FilesToConvert/*
        working_directory = 'WorkingFiles/FilesToConvert'
        for file in os.scandir(working_directory):
            os.remove(file.path)

    @_convert_audio_.error
    async def _convert_error(self, ctx, error):
        if isinstance(error, discord.HTTPException):
            await ctx.send(f'{ctx.author.mention}, saving your attachment failed.', delete_after=10)
        elif isinstance(error, discord.NotFound):
            await ctx.send(f'{ctx.author.mention}, no attachments were found to convert.', delete_after=10)

    # Makes and uploads files bases on user's decision
    @commands.command(name='combine')
    async def _combine_files_(self, ctx):
        if ctx.message.attachments:
            await ctx.send(f'{ctx.author.mention}, I am processing your request...', delete_after=3)
            pdf_check = ['.pdf']
            # Check if attatched file is .pdf
            for attachment in ctx.message.attachments:
                attatched_file_type = (os.path.splitext(str(attachment))[1])
                if attatched_file_type not in pdf_check:
                    await ctx.send(f'{ctx.author.mention}, the file(s) attached is not a PDF. Currently only PDF combinations are supported.', delete_after=10)
                    break

            # Ensures the FilesToCombine directory exists
            path = 'WorkingFiles/FilesToCombine/'
            directory_exists = os.path.exists(path)
            if directory_exists is False:
                os.mkdir(path)

            merger = PdfFileMerger()
            for pdf in ctx.message.attachments:
                # Download the user attachments on iterator through list
                await pdf.save(f'WorkingFiles/FilesToCombine/{pdf.filename}')
                # Input file
                input_filepath = f'WorkingFiles/FilesToCombine/{pdf.filename}'
                # Appends each file attached to the PDF merger
                merger.append(input_filepath)

            # Output file
            out_file = 'WorkingFiles/FilesToCombine/ChetBot_Combined.pdf'
            # The PDF merger takes all appended files and writes them to the outfile
            merger.write(out_file)
            # Send combined file
            await ctx.send(file=discord.File(out_file))

            # Must sleep (20s) to prevent possible errors with the deletion of files
            await asyncio.sleep(20)
            # After output is sent, delete WorkingFiles/FilesToConvert/*
            working_directory = 'WorkingFiles/FilesToCombine'
            for file in os.scandir(working_directory):
                os.remove(file.path)


async def setup(ChetBot):
    await ChetBot.add_cog(FileOperations(ChetBot))
