import os
import platform
import subprocess
from typing import Optional

import discord
from PyPDF2 import PdfFileMerger
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import parameter
from pyffmpeg import FFmpeg
from yt_dlp import YoutubeDL

from functions import file_conversion, getTime, removeDirectory


class FileOperations(commands.Cog, name='File Commands', description='File Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Makes and uploads files bases on user's decision
    @commands.hybrid_group(name='delimited', with_app_command=True, description='Creates and uploads a file based on the user\'s descision.\n/delimited <desired_file_type> <user_input>')
    async def _create_file_(self, ctx: commands.Context) -> None:
        print('I am the parent delimited command')

    @_create_file_.command(name='csv', with_app_command=True, description='Creates a csv delimited file based on user input.')
    @app_commands.describe(where_to_split='Optional character to split your input on',
                           user_input='Any input given by the user to be added to the file')
    async def _create_file_csv_(self, ctx: commands.Context, *, where_to_split: str = parameter(default=' ', description='- Optional character to split your input on'), user_input: str = parameter(description='- Any input given by the user to be added to the file')) -> None:

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/FilesToCreate/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        exists_already = os.path.exists(temp_directory)
        # Ensure no errors from file already exists
        if exists_already:
            os.rmdir(temp_directory)
        os.mkdir(temp_directory)

        working_file = f'{temp_directory}/ChetBot.csv'
        space_seperated = user_input.split(where_to_split)
        working_text = ', '.join(space_seperated)
        f = open(working_file, "w")
        f.write(working_text)
        f.close()
        await ctx.send(file=discord.File(working_file))
        removeDirectory(temp_directory)

    @_create_file_.command(name='tab', with_app_command=True, description='Creates a tab delimited file based on user input.')
    @app_commands.describe(where_to_split='Optional character to split your input on',
                           user_input='Any input given by the user to be added to the file')
    async def _create_file_csv_(self, ctx: commands.Context, *, where_to_split: str = parameter(default=' ', description='- Optional character to split your input on'), user_input: str = parameter(description='- Any input given by the user to be added to the file')) -> None:

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/FilesToCreate/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        exists_already = os.path.exists(temp_directory)
        # Ensure no errors from file already exists
        if exists_already:
            os.rmdir(temp_directory)
        os.mkdir(temp_directory)

        working_file = f'{temp_directory}/ChetBot.csv'
        space_seperated = user_input.split(where_to_split)
        working_text = '\t'.join(space_seperated)
        f = open(working_file, "w")
        f.write(working_text)
        f.close()
        await ctx.send(file=discord.File(working_file))
        removeDirectory(temp_directory)

    @_create_file_.command(name='line', with_app_command=True, description='Creates a line delimited file based on user input.')
    @app_commands.describe(where_to_split='Optional character to split your input on',
                           user_input='Any input given by the user to be added to the file')
    async def _create_file_csv_(self, ctx: commands.Context, *, where_to_split: str = parameter(default=' ', description='- Optional character to split your input on'), user_input: str = parameter(description='- Any input given by the user to be added to the file')) -> None:

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/FilesToCreate/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        exists_already = os.path.exists(temp_directory)
        # Ensure no errors from file already exists
        if exists_already:
            os.rmdir(temp_directory)
        os.mkdir(temp_directory)

        working_file = f'{temp_directory}/ChetBot.csv'
        space_seperated = user_input.split(where_to_split)
        working_text = '\n'.join(space_seperated)
        f = open(working_file, "w")
        f.write(working_text)
        f.close()
        await ctx.send(file=discord.File(working_file))
        removeDirectory(temp_directory)

    # Coverts user attachments to desired type
    @commands.hybrid_command(name='convert', with_app_command=True, description='Converts user attached file from specified initial type to specified desired type.')
    @app_commands.describe(initial_file_type='Options are: [pdf | docx | jpg | jpeg | png]',
                           desired_file_type='Options are: [pdf | docx | jpg | jpeg | png]',
                           attachment1='The attachment to convert.',
                           attachment2='The attachment to convert.',
                           attachment3='The attachment to convert.',
                           attachment4='The attachment to convert.',
                           attachment5='The attachment to convert.',
                           attachment6='The attachment to convert.',
                           attachment7='The attachment to convert.',
                           attachment8='The attachment to convert.',
                           attachment9='The attachment to convert.',
                           attachment10='The attachment to convert.')
    async def _convert_files_(self, ctx: commands.Context,
                              initial_file_type: str = parameter(description='- Options are: [pdf | docx | jpg | jpeg | png]'),
                              desired_file_type: str = parameter(description='- Options are: [pdf | docx | jpg | jpeg | png]'),
                              attachment1: discord.Attachment = parameter(description=' - The attachment to convert.'),
                              attachment2: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment3: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment4: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment5: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment6: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment7: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment8: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment9: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment10: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.')) -> None:
        await ctx.typing()
        if ctx.message.attachments:

            # Defining variables in use
            initial_check = f'/{initial_file_type}'
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
                    await ctx.send(f'{ctx.author.mention}, the type of file attached is not currently supported.', delete_after=10)
                # Checks if the initial declared value matched actual uploaded attachment file type
                for working_file in range(0, limit + 1):
                    working_file_attachment = str(ctx.message.attachments[working_file].content_type)
                    if initial_check in working_file_attachment:
                        type_check = initial_check in working_file_attachment
                        check_counter = check_counter + 1

                    elif initial_check not in working_file_attachment:
                        await ctx.send(
                            f'{ctx.author.mention}, the initial file type you declared doesn\'t match the file type of the attachment.', delete_after=10)
                        break

                    if check_counter == limit:
                        break

                # Make unique temporary directory to use for each user
                parent_dir = 'WorkingFiles/FilesToConvert/'
                user_dir = str(ctx.author.id)
                temp_directory = os.path.join(parent_dir, user_dir)
                exists_already = os.path.exists(temp_directory)
                # Ensure no errors from file already exists
                if exists_already:
                    os.rmdir(temp_directory)
                os.mkdir(temp_directory)

                # Prevents possible user error where user clicks wrong attachment number
                default_attachment_list = [attachment1, attachment2, attachment3, attachment4, attachment5,
                                           attachment6, attachment7, attachment8, attachment9, attachment10]
                actual_attachment_list = []
                for x in (range(0, len(default_attachment_list))):
                    if default_attachment_list[x] is not None:
                        actual_attachment_list.append(default_attachment_list[x])

                if type_check:
                    await ctx.send(f'{ctx.author.mention}, I am processing your request...', delete_after=3)
                    for attachment in tuple(actual_attachment_list):
                        # Download the user attachments on iterator through list
                        await attachment.save(f'{temp_directory}/{attachment.filename}')
                        # Input file
                        input_filepath = f'{temp_directory}/{attachment.filename}'
                        # Output file
                        outfile = file_conversion(input_filepath, desired_file_type)
                        if outfile is None:
                            await ctx.send(
                                f'{ctx.author.mention}, the file conversion you attempted is not currently supported.',
                                delete_after=10)
                            break
                        elif outfile is not None:
                            await ctx.send(file=discord.File(outfile))
            else:
                await ctx.send(
                    f'{ctx.author.mention}, the initial file type you declared doesn\'t match the file type of the attachment.',
                    delete_after=10)
        else:
            await ctx.send(f'{ctx.author.mention}, no attachments were found to convert.', delete_after=10)

        # Remove temporary user directory
        removeDirectory(temp_directory)

    # Coverts user audio attachments from allowed types
    @commands.hybrid_command(name='audio', with_app_command=True, description='Converts user attached audio or video file from specified initial type to specified desired type.')
    @app_commands.describe(initial_file_type='Options are: [mp4 | mp3 | wav]',
                           desired_file_type='Options are: [mp4 | mp3 | wav]',
                           attachment1='The attachment to convert.',
                           attachment2='The attachment to convert.',
                           attachment3='The attachment to convert.',
                           attachment4='The attachment to convert.',
                           attachment5='The attachment to convert.',
                           attachment6='The attachment to convert.',
                           attachment7='The attachment to convert.',
                           attachment8='The attachment to convert.',
                           attachment9='The attachment to convert.',
                           attachment10='The attachment to convert.')
    async def _convert_audio_(self, ctx: commands.Context,
                              initial_file_type: str = parameter(description='- Options are: [mp4 | mp3 | wav]'),
                              desired_file_type: str = parameter(description='- Options are: [mp4 | mp3 | wav]'),
                              attachment1: discord.Attachment = parameter(description=' - The attachment to convert.'),
                              attachment2: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment3: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment4: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment5: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment6: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment7: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment8: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment9: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.'),
                              attachment10: Optional[discord.Attachment] = parameter(default=None, description=' - The attachment to convert.')) -> None:
        await ctx.typing()
        if ctx.message.attachments:

            # Defining variables in use
            initial_check = f'/{initial_file_type}'
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

                # Make unique temporary directory to use for each user
                parent_dir = 'WorkingFiles/FilesToConvert/'
                user_dir = str(ctx.author.id)
                temp_directory = os.path.join(parent_dir, user_dir)
                exists_already = os.path.exists(temp_directory)
                # Ensure no errors from file already exists
                if exists_already:
                    os.rmdir(temp_directory)
                os.mkdir(temp_directory)

                # Prevents possible user error where user clicks wrong attachment number
                default_attachment_list = [attachment1, attachment2, attachment3, attachment4, attachment5,
                                           attachment6, attachment7, attachment8, attachment9, attachment10]
                actual_attachment_list = []
                for x in (range(0, len(default_attachment_list))):
                    if default_attachment_list[x] is not None:
                        actual_attachment_list.append(default_attachment_list[x])

                if type_check:
                    await ctx.send(f'{ctx.author.mention}, I am processing your request...', delete_after=5)
                    for attachment in tuple(actual_attachment_list):
                        # Download the user attachments on iterator through list
                        await attachment.save(f'{temp_directory}/{attachment.filename}')
                        # Keeping the file name uploaded by the user without the previous unconverted extension
                        trimmed_filename = (os.path.splitext(str(attachment.filename))[0])
                        # Input file
                        input_filepath = f'{temp_directory}/{attachment.filename}'
                        # Output file
                        output_filepath = f'{temp_directory}/{trimmed_filename}.{desired_file_type}'
                        operating_system = platform.system()
                        # Checking OS as ffmpeg is called differently on each
                        if operating_system == 'Windows':
                            # Defining ff to FFmpeg
                            ff = FFmpeg()
                            # Setting the conversion as the downloaded user file, to the desired user file type
                            out_file = ff.convert(input_filepath, output_filepath)
                            await ctx.send(file=discord.File(out_file))
                        elif operating_system == 'Linux':
                            subprocess.run(['ffmpeg', '-i', input_filepath, output_filepath], shell=False)
                            await ctx.send(file=discord.File(output_filepath))
            else:
                await ctx.send(
                    f'{ctx.author.mention}, the initial file type you declared doesn\'t match the file type of the attachment.',
                    delete_after=10)
        else:
            await ctx.send(f'{ctx.author.mention}, no attachments were found to convert.', delete_after=10)

        # Remove temporary user directory
        removeDirectory(temp_directory)

    # Makes and uploads files bases on user's decision
    @commands.hybrid_command(name='combine', with_app_command=True, description='Combines user attached PDF files.')
    @app_commands.describe(attachment1='The attachment to combine.',
                           attachment2='The attachment to combine.',
                           attachment3='The attachment to combine.',
                           attachment4='The attachment to combine.',
                           attachment5='The attachment to combine.',
                           attachment6='The attachment to combine.',
                           attachment7='The attachment to combine.',
                           attachment8='The attachment to combine.',
                           attachment9='The attachment to combine.',
                           attachment10='The attachment to combine.')
    async def _combine_files_(self, ctx: commands.Context,
                              attachment1: discord.Attachment,
                              attachment2: discord.Attachment,
                              attachment3: Optional[discord.Attachment] = parameter(default=None),
                              attachment4: Optional[discord.Attachment] = parameter(default=None),
                              attachment5: Optional[discord.Attachment] = parameter(default=None),
                              attachment6: Optional[discord.Attachment] = parameter(default=None),
                              attachment7: Optional[discord.Attachment] = parameter(default=None),
                              attachment8: Optional[discord.Attachment] = parameter(default=None),
                              attachment9: Optional[discord.Attachment] = parameter(default=None),
                              attachment10: Optional[discord.Attachment] = parameter(default=None)) -> None:
        if len(ctx.message.attachments) >= 2:
            await ctx.send(f'{ctx.author.mention}, I am processing your request...', delete_after=5)
            # Check if attached file is .pdf
            for attachment in ctx.message.attachments:
                attached_file_type = (os.path.splitext(str(attachment))[1])
                if attached_file_type not in ['.pdf']:
                    await ctx.send(f'{ctx.author.mention}, one or more of the files attached is not a PDF. Currently only PDF combinations are supported.', delete_after=10)
                    break

            # Make unique temporary directory to use for each user
            parent_dir = 'WorkingFiles/FilesToCombine/'
            user_dir = str(ctx.author.id)
            temp_directory = os.path.join(parent_dir, user_dir)
            exists_already = os.path.exists(temp_directory)
            # Ensure no errors from file already exists
            if exists_already:
                os.rmdir(temp_directory)
            os.mkdir(temp_directory)

            merger = PdfFileMerger()
            # Prevents possible user error where user clicks wrong attachment number
            default_attachment_list = [attachment1, attachment2, attachment3, attachment4, attachment5,
                                       attachment6, attachment7, attachment8, attachment9, attachment10]
            actual_attachment_list = []
            for x in (range(0, len(default_attachment_list))):
                if default_attachment_list[x] is not None:
                    actual_attachment_list.append(default_attachment_list[x])

            for pdf in tuple(actual_attachment_list):
                # Download the user attachments on iterator through the attachment list that is cast as a tuple
                await pdf.save(f'{temp_directory}/{pdf.filename}')
                # Input file
                input_filepath = f'{temp_directory}/{pdf.filename}'
                # Appends each file attached to the PDF merger
                merger.append(input_filepath)

            # Output file
            out_file = f'{temp_directory}/ChetBotCombined.pdf'

            # Check if uploaded file name is already that of the outfile to avoid errors
            if os.path.isfile(out_file):
                current_time = getTime('-')
                out_file = f'{temp_directory}/ChetBotCombined-{current_time}.pdf'

            # The PDF merger takes all appended files and writes them to the outfile
            merger.write(out_file)
            # Need to close merger or files won't get deleted in WorkingFiles/FilesToCombine/
            merger.close()
            # Send combined file
            await ctx.send(file=discord.File(out_file))

        elif len(ctx.message.attachments) in [0, 1]:
            await ctx.send(f'{ctx.author.mention}, you must attach 2 or more pdf files for me to combine them.', delete_after=10)

        # Remove temporary user directory
        removeDirectory(temp_directory)

    # Downloads a YouTube Video to desired output
    @commands.hybrid_group(name='youtube', with_app_command=True, description='Downloads and/or converts a YouTube video from the URL given to the requested type.')
    async def _youtube_command_(self, ctx: commands.Context) -> None:
        print(f'I am the parent YouTube command')

    @_youtube_command_.command(name='mp3', with_app_command=True, description='Downloads and converts a YouTube video from the URL given to an mp3.')
    @app_commands.describe(url='The YouTube URL that you would like ChetBot to download')
    async def _youtube_download_mp3_(self, ctx: commands.Context, url: str = parameter(description='- The YouTube URL that you would like ChetBot to download')) -> None:

        await ctx.send(f'{ctx.author.mention}, your request is being processed...')

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/FilesToUpload/'
        user_dir = str(ctx.author.id)

        temp_directory = os.path.join(parent_dir, user_dir)
        exists_already = os.path.exists(temp_directory)
        # Ensure no errors from file already exists
        if exists_already:
            os.rmdir(temp_directory)
        os.mkdir(temp_directory)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': temp_directory + '/%(title)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir(temp_directory):
            await ctx.reply(file=discord.File(f'{temp_directory}/{file}'))

        # Remove temporary user directory
        removeDirectory(temp_directory)

    # Hidden from view as it must be under 8MiB to send, still works locally or under 8 MiB; I am not removing the rule
    @_youtube_command_.command(name='mp4', hidden=True, with_app_command=False, description='Downloads and converts a YouTube video from the URL given to an mp4.')
    @app_commands.describe(url='The YouTube URL that you would like ChetBot to download')
    async def _youtube_download_mp4_(self, ctx: commands.Context, url: str = parameter(description='- The YouTube URL that you would like ChetBot to download')) -> None:

        await ctx.send(f'{ctx.author.mention}, your request is being processed...')

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/FilesToUpload/'
        user_dir = str(ctx.author.id)

        temp_directory = os.path.join(parent_dir, user_dir)
        exists_already = os.path.exists(temp_directory)
        # Ensure no errors from file already exists
        if exists_already:
            os.rmdir(temp_directory)
        os.mkdir(temp_directory)

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': temp_directory + '/%(title)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir(temp_directory):
            await ctx.reply(file=discord.File(f'{temp_directory}/{file}'))


async def setup(ChetBot):
    await ChetBot.add_cog(FileOperations(ChetBot))
