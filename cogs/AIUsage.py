import os

import discord
import whisper
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import parameter

from functions import removeDirectory


class AI(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # To lowercase
    @app_commands.command(name='transcribe-audio', description='Transcribes the attached audio file.')
    @app_commands.describe(attachment='Audio file to transcribe.')
    async def _transcribe_audio_(self, interaction: discord.Interaction, attachment: discord.Attachment) -> None:
        if attachment:
            # Make unique temporary directory to use for each user
            parent_dir = 'WorkingFiles/FilesToConvert/'
            user_dir = str(interaction.user.id)
            temp_directory = os.path.join(parent_dir, user_dir)

            exists_already = os.path.exists(temp_directory)
            # Ensure no errors from file already exists
            if exists_already:
                os.rmdir(temp_directory)
            os.mkdir(temp_directory)

            # Input file
            input_filepath = f'{temp_directory}/{attachment.filename}'
            await attachment.save(f'{input_filepath}')

            # Keeping the file name uploaded by the user without the previous unconverted extension
            trimmed_filename = (os.path.splitext(str(attachment.filename))[0])

            # Output file
            output_file = f'{temp_directory}/{trimmed_filename}.txt'

            # Setup OpenAI's Whisper // https://github.com/openai/whisper
            model = whisper.load_model("base")

            # load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(input_filepath)
            audio = whisper.pad_or_trim(audio)

            # make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(model.device)

            with open(output_file, 'w') as file:
                # detect the spoken language
                _, probs = model.detect_language(mel)
                file.write(f'Detected language of speaker in audio file provided:\n[{max(probs, key=probs.get)}]\n\n')
                # decode the audio
                options = whisper.DecodingOptions(fp16=False)
                result = whisper.decode(model, mel, options)
                file.write(f'Transcription:\n[{result.text}]')

            await interaction.response.send_message(f'{interaction.user.mention}, here is the transcription I generated for you from the provided input file [{attachment.filename}]:', file=discord.File(output_file), ephemeral=True)

            # Remove temporary user directory
            removeDirectory(temp_directory)
        else:
            await interaction.response.send_message(f'{interaction.user.mention}, you did not attach a file. Please ensure that you add a file to your `/transcribe` command.')


async def setup(ChetBot):
    await ChetBot.add_cog(AI(ChetBot))
