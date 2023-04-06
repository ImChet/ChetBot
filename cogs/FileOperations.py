import os
import subprocess
from typing import Optional

import discord
from PyPDF2 import PdfMerger
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import parameter
from yt_dlp import YoutubeDL

from functions import removeDirectory


# The Custom Button for the Audio Conversion Options
class AudioConversionOptionButton(discord.ui.Button):
    def __init__(self, **kwargs):
        self.clicked = False
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction):
        view: AudioConversionOptionsButtonView = self.view
        # Append each chosen option to the 'ordered_list' variable
        view.chosen_option = self.label
        for button in view.killable_buttons_list:
            button.clicked = True
            button.disabled = True
            button.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(view=view)


# The Confirm Selection Custom Button for the Audio Conversion Options
class ConfirmAudioSelectionButton(discord.ui.Button):
    def __init__(self, **kwargs):
        self.clicked = False
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction):
        view: AudioConversionOptionsButtonView = self.view
        # Set each button to be disabled as the results are now confirmed but the user
        for child in view.children:
            child.clicked = True
            child.disabled = True
            child.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(view=view)

        # Input filepath(s) list
        input_local_filepaths_list = view.local_filepaths_list
        # Output filepath(s) list
        output_local_filepaths_list = []

        for filepath in input_local_filepaths_list:
            clean_filename = (os.path.splitext(str(filepath))[0]).replace(f'{view.temp_directory}/', '')
            print(f'clean_filename: {clean_filename}')
            output_local_filepaths_list.append(f'{view.temp_directory}/{clean_filename}{view.chosen_option}')
            print(f'output_local_filepaths_list: {output_local_filepaths_list}')

        if len(input_local_filepaths_list) == len(output_local_filepaths_list):
            for i in range(len(input_local_filepaths_list)):
                # Input file
                input_filepath = input_local_filepaths_list[i]
                # Output file
                output_filepath = output_local_filepaths_list[i]
                # Run ffmpeg conversion through subprocess
                subprocess.run(['ffmpeg', '-i', input_filepath, output_filepath], shell=False)

            for item in output_local_filepaths_list:
                await interaction.followup.send(file=discord.File(item), ephemeral=True)

        exists_already = os.path.exists(view.temp_directory)
        if exists_already:
            removeDirectory(view.temp_directory)


# The view for all the Audio Conversion Options
class AudioConversionOptionsButtonView(discord.ui.View):
    def __init__(self, temp_directory, local_filepaths_list):
        self.chosen_option = None
        self.audio_options_list = ['.flac', '.wav', '.mp3', '.avi', '.aac', '.ac3']
        self.killable_buttons_list = []
        self.temp_directory = temp_directory
        self.local_filepaths_list = local_filepaths_list
        super().__init__()
        self.value = None

        # Create the Confirm Selection
        confirm_button = ConfirmAudioSelectionButton(label='Confirm Selection', custom_id='Confirm Selection', style=discord.ButtonStyle.green)
        self.add_item(confirm_button)

        for item in self.audio_options_list:
            button = AudioConversionOptionButton(style=discord.ButtonStyle.blurple, label=item, custom_id=item)
            self.killable_buttons_list.append(button)
            self.add_item(button)

    # Reset Selection button to allow for potential user error
    @discord.ui.button(label='Reset Selection', style=discord.ButtonStyle.red)
    async def _reset_button_(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Resets the chosen_option
        self.chosen_option = None
        # Through a list go and re-enable the buttons for the user to click on again
        for child in self.killable_buttons_list:
            child.disabled = False
            child.clicked = False
            child.style = discord.ButtonStyle.blurple
        await interaction.response.edit_message(view=self)


# Need custom callback operation for File Order Buttons // For PDFCombiner
class FileOrderPDFCombinerButton(discord.ui.Button):
    def __init__(self, **kwargs):
        self.clicked = False
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction):
        view: FileOrderButtonPDFCombinerView = self.view
        # Append each chosen option to the 'ordered_list' variable
        view.ordered_list.append(self.label)
        # Set each button to be disabled as the results are now confirmed but the user
        self.clicked = True
        self.disabled = True
        self.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(view=view)


# Need custom callback operation for Confirm Selection Button // For PDFCombiner
class ConfirmSelectionPDFCombinerButton(discord.ui.Button):
    def __init__(self, **kwargs):
        self.clicked = False
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction):
        view: FileOrderButtonPDFCombinerView = self.view
        # Set each button to be disabled as the results are now confirmed but the user
        for child in view.children:
            child.clicked = True
            child.disabled = True
            child.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(view=view)

        # Start the PDF merger
        merger = PdfMerger()
        # Append each file to the new combined PDF
        for file in view.local_file_paths:
            merger.append(file)
        # Output file
        out_file = f'{view.temp_directory}/ChetBotCombined.pdf'
        # The PDF merger takes all appended files and writes them to the outfile
        merger.write(out_file)
        # Close the merger
        merger.close()

        # Send user the combined file via a followup otherwise interaction gets too many responses
        await interaction.followup.send(file=discord.File(out_file), ephemeral=True)

        # Remove temporary user directory
        removeDirectory(view.temp_directory)


# Defines the File Order Button Schema View // For PDFCombiner
class FileOrderButtonPDFCombinerView(discord.ui.View):
    def __init__(self, temp_directory, local_file_paths):
        self.temp_directory = temp_directory
        self.local_file_paths = local_file_paths
        # Assign each user submitted attachment as a self.file{i} variable
        for i, arg in enumerate(local_file_paths):
            setattr(self, f'file_{i}', arg)
        super().__init__()
        # Empty lists to use
        self.ordered_list = []
        self.resettable_button_list = []

        # Create the Confirm Selection
        confirm_button = ConfirmSelectionPDFCombinerButton(label='Confirm Selection', custom_id='Confirm Selection', style=discord.ButtonStyle.blurple)
        self.add_item(confirm_button)

        # Create and add the file-specific buttons with cleaned names
        for i in range(len(local_file_paths)):
            button_label = f'{getattr(self, f"file_{i}")}'
            button_label_cleaned = button_label.replace(f'{temp_directory}/', '')
            button = FileOrderPDFCombinerButton(style=discord.ButtonStyle.green, label=button_label_cleaned, custom_id=f'{getattr(self, f"file_{i}")}')
            self.resettable_button_list.append(button)
            self.add_item(button)

    # Reset Selection button to allow for potential user error
    @discord.ui.button(label='Reset Selection', style=discord.ButtonStyle.red)
    async def _reset_button_(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Resets the ordered list
        self.ordered_list = []
        # Through a list go and re-enable the buttons for the user to click on again
        for child in self.resettable_button_list:
            child.disabled = False
            child.clicked = False
            child.style = discord.ButtonStyle.green
        await interaction.response.edit_message(view=self)


# Main FileOperations Cog
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
            removeDirectory(temp_directory)
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
            removeDirectory(temp_directory)
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
            removeDirectory(temp_directory)
        os.mkdir(temp_directory)

        working_file = f'{temp_directory}/ChetBot.csv'
        space_seperated = user_input.split(where_to_split)
        working_text = '\n'.join(space_seperated)
        f = open(working_file, "w")
        f.write(working_text)
        f.close()
        await ctx.send(file=discord.File(working_file))
        removeDirectory(temp_directory)

    # Coverts user audio attachments from allowed types // Changed back to non-slash command to allow more enhanced features in the future
    @app_commands.command(name='convert-audio', description='Converts user attached video/audio file(s) to the desired audio file type.')
    @app_commands.describe(attachment1='The video/audio file to convert.',
                           attachment2='The video/audio file to convert.',
                           attachment3='The video/audio file to convert.',
                           attachment4='The video/audio file to convert.',
                           attachment5='The video/audio file to convert.',
                           attachment6='The video/audio file to convert.',
                           attachment7='The video/audio file to convert.',
                           attachment8='The video/audio file to convert.',
                           attachment9='The video/audio file to convert.',
                           attachment10='The video/audio file to convert.')
    async def _convert_audio_(self, interaction: discord.Interaction,
                              attachment1: discord.Attachment,
                              attachment2: Optional[discord.Attachment] = None,
                              attachment3: Optional[discord.Attachment] = None,
                              attachment4: Optional[discord.Attachment] = None,
                              attachment5: Optional[discord.Attachment] = None,
                              attachment6: Optional[discord.Attachment] = None,
                              attachment7: Optional[discord.Attachment] = None,
                              attachment8: Optional[discord.Attachment] = None,
                              attachment9: Optional[discord.Attachment] = None,
                              attachment10: Optional[discord.Attachment] = None) -> None:
        default_attachment_list = [attachment1, attachment2, attachment3, attachment4, attachment5, attachment6, attachment7, attachment8, attachment9, attachment10]
        actual_attachment_list = []
        # Get the actual attachments submitted by the user, fixes possible user error
        for x in (range(0, len(default_attachment_list))):
            if default_attachment_list[x] is not None:
                actual_attachment_list.append(default_attachment_list[x])
        # Assure that there are >=1 attachments submitted
        if len(actual_attachment_list) >= 1:

            supported_check = True
            for attachment in actual_attachment_list:
                attached_file_type = (os.path.splitext(str(attachment))[1])
                if attached_file_type not in ['.flac', '.wav', '.mp3', '.avi', '.aac', '.ac3', '.mp4', '.oog']:
                    supported_check = False
                    break

            if supported_check is True:
                # Make unique temporary directory to use for each user
                parent_dir = 'WorkingFiles/FilesToConvert/'
                user_dir = str(interaction.user.id)
                temp_directory = os.path.join(parent_dir, user_dir)
                exists_already = os.path.exists(temp_directory)
                # Ensure no errors from file already exists
                if exists_already:
                    removeDirectory(temp_directory)
                os.mkdir(temp_directory)

                # Local filepath of downloaded file(s) list
                local_filepaths_list = []

                # Download the user attachments on iterator through list
                for attachment in actual_attachment_list:
                    filepath = f'{temp_directory}/{attachment.filename}'
                    local_filepaths_list.append(filepath)
                    await attachment.save(filepath)

                await interaction.response.send_message(f'{interaction.user.mention}, choose what file type that you would like your uploaded file(s) to be converted to, then confirm your selection...', view=AudioConversionOptionsButtonView(temp_directory, local_filepaths_list), ephemeral=True)
            else:
                await interaction.response.send_message(f'{interaction.user.mention}, disallowed input file type detected.\nCurrently only `.flac`, `.wav`, `.mp3`, `.avi`, `.aac`, `.ac3`, `.mp4`, and `.oog` input file types are supported. Please try again.', ephemeral=True)

    # Combines user attached PDFs
    @app_commands.command(name='pdf-combine', description='Combines user attached PDF files.')
    @app_commands.describe(attachment1='The pdf to combine.',
                           attachment2='The pdf to combine.',
                           attachment3='The pdf to combine.',
                           attachment4='The pdf to combine.',
                           attachment5='The pdf to combine.',
                           attachment6='The pdf to combine.',
                           attachment7='The pdf to combine.',
                           attachment8='The pdf to combine.',
                           attachment9='The pdf to combine.',
                           attachment10='The pdf to combine.')
    async def _pdf_file_combine_(self, interaction: discord.Interaction,
                                 attachment1: discord.Attachment,
                                 attachment2: discord.Attachment,
                                 attachment3: Optional[discord.Attachment] = None,
                                 attachment4: Optional[discord.Attachment] = None,
                                 attachment5: Optional[discord.Attachment] = None,
                                 attachment6: Optional[discord.Attachment] = None,
                                 attachment7: Optional[discord.Attachment] = None,
                                 attachment8: Optional[discord.Attachment] = None,
                                 attachment9: Optional[discord.Attachment] = None,
                                 attachment10: Optional[discord.Attachment] = None) -> None:
        default_attachment_list = [attachment1, attachment2, attachment3, attachment4, attachment5, attachment6,
                                   attachment7, attachment8, attachment9, attachment10]

        actual_attachment_list = []
        # Get the actual attachments submitted by the user, fixes possible user error
        for x in (range(0, len(default_attachment_list))):
            if default_attachment_list[x] is not None:
                actual_attachment_list.append(default_attachment_list[x])

        # Assure that there are >2 attachments submitted
        if len(actual_attachment_list) >= 2:
            # Check if attached file is .pdf
            supported_check = True
            for attachment in actual_attachment_list:
                attached_file_type = (os.path.splitext(str(attachment))[1])
                if attached_file_type not in ['.pdf']:
                    supported_check = False
                    break
            if supported_check is True:
                # Make unique temporary directory to use for each user
                parent_dir = 'WorkingFiles/FilesToCombine/'
                user_dir = str(interaction.user.id)
                temp_directory = os.path.join(parent_dir, user_dir)
                exists_already = os.path.exists(temp_directory)
                # Ensure no errors from file already exists
                if exists_already:
                    removeDirectory(temp_directory)
                os.mkdir(temp_directory)
                # Declare relative local filepaths to use
                file_paths_to_use_list = []
                # Ensure no duplicate file names with set()
                filename_set = set()
                # Duplicate flag
                duplicate_filename = False
                # Get filepaths from discord and download them
                for file in actual_attachment_list:
                    current_file = f'{temp_directory}/{file.filename}'
                    # Check if filename is already in the set
                    if file.filename in filename_set:
                        duplicate_filename = True
                        break
                    else:
                        filename_set.add(file.filename)
                        await file.save(current_file)
                        file_paths_to_use_list.append(str(current_file))
                if duplicate_filename:
                    removeDirectory(temp_directory)
                    await interaction.response.send_message(f'{interaction.user.mention}, duplicate file names were detected. Please ensure that each filename is unique and try again.', ephemeral=True)
                else:
                    # Send 'file_paths_to_use_list' to the FileOrderButtonPDFCombinerView
                    view = FileOrderButtonPDFCombinerView(temp_directory, file_paths_to_use_list)
                    await interaction.response.send_message(f'{interaction.user.mention}, please click the order in which you would like your attachments combined, then confirm your selection...', view=view, ephemeral=True)
                    await view.wait()
            else:
                await interaction.response.send_message(f'{interaction.user.mention}, one or more of the files attached is not a `.pdf`. Currently only `.pdf` combinations are supported.', ephemeral=True)
        else:
            await interaction.response.send_message(f'{interaction.user.mention}, you must attach 2 or more `.pdf` files for me to combine them.', ephemeral=True)

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
            removeDirectory(temp_directory)
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
            removeDirectory(temp_directory)
        os.mkdir(temp_directory)

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': temp_directory + '/%(title)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir(temp_directory):
            await ctx.reply(file=discord.File(f'{temp_directory}/{file}'))

        # Remove temporary user directory
        removeDirectory(temp_directory)


async def setup(ChetBot):
    await ChetBot.add_cog(FileOperations(ChetBot))
