import os

import discord
from discord import FFmpegPCMAudio, app_commands
from discord.ext import commands
from discord.ext.commands import parameter
from yt_dlp import YoutubeDL

from functions import check_queue, queues, checkDirectoryExists, checkDirectoryExistsDelete, randomChar


class VoiceChannel(commands.Cog, name='Voice Channel Commands', description='Voice Channel Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Defining the 'voice' hybrid group command
    @commands.hybrid_group(name='voice', with_app_command=True, description='Voice channel commands for ChetBot to execute.')
    @app_commands.guilds(495623660967690240)
    async def _voice_(self, ctx: commands.Context) -> None:
        print('I am the parent voice command')

    # Join voice channel
    @_voice_.command(name='join', with_app_command=True, description='Makes ChetBot join the Voice Channel that you are currently in.')
    @app_commands.guilds(495623660967690240)
    async def _join_(self, ctx: commands.Context) -> None:
        if ctx.author.voice:
            await ctx.message.author.voice.channel.connect()
            await ctx.send(f'I have connected to the voice channel.', delete_after=5)

            # Removes the temp directory if still exists
            parent_dir = 'WorkingFiles/AudioFilesToUse/'
            user_dir = str(ctx.author.id)
            temp_directory = os.path.join(parent_dir, user_dir)
            checkDirectoryExistsDelete(temp_directory)
        else:
            await ctx.send(f'{ctx.author.mention}, you are not in a voice channel.', delete_after=10)

    # Leave voice channel
    @_voice_.command(name='leave', with_app_command=True, description='Makes ChetBot leave the Voice Channel that you are currently in.')
    @app_commands.guilds(495623660967690240)
    async def _leave_(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send(f'I have disconnected from the voice channel.', delete_after=5)

            # Removes the temp directory if music is stopped this way
            parent_dir = 'WorkingFiles/AudioFilesToUse/'
            user_dir = str(ctx.author.id)
            temp_directory = os.path.join(parent_dir, user_dir)
            checkDirectoryExistsDelete(temp_directory)
        else:
            await ctx.send(f'{ctx.author.mention}, I am not in a voice channel.', delete_after=10)

    # Play file located at audio
    @_voice_.command(name='play', with_app_command=True, description='Makes ChetBot play audio.')
    @app_commands.guilds(495623660967690240)
    async def _play_(self, ctx: commands.Context, url: str = parameter(description='- The YouTube URL that you would like ChetBot to play')) -> None:
        if ctx.guild.voice_client is None:
            if ctx.author.voice:
                await ctx.message.author.voice.channel.connect()
                await ctx.send(f'I have connected to the voice channel.', delete_after=5)

                # Removes the temp directory if still exists to avoid errors
                parent_dir = 'WorkingFiles/AudioFilesToUse/'
                user_dir = str(ctx.author.id)
                temp_directory = os.path.join(parent_dir, user_dir)
                checkDirectoryExistsDelete(temp_directory)
            else:
                await ctx.send(f'{ctx.author.mention}, you are not in a voice channel.', delete_after=10)

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/AudioFilesToUse/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        os.mkdir(temp_directory)

        working_file = f'{temp_directory}/{randomChar(10)}.mp3'

        await ctx.send(f'{ctx.author.mention}, your song is being processed...', delete_after=5)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': working_file,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # source = FFmpegPCMAudio(working_file)
        working_file_list = [working_file]
        voice = ctx.guild.voice_client

        for file in working_file_list:
            source = FFmpegPCMAudio(file)
            voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
            await ctx.send(f'I started playing your requested audio.', delete_after=5)

        # I do not think you are able to get this part to ever trigger after the queue is empty
        # and the bot is not playing audio
        # removeDirectory(temp_directory)

    # Queues next YouTube video
    @_voice_.command(name='queue', with_app_command=True, description='Makes ChetBot queue audio to play next.')
    @app_commands.guilds(495623660967690240)
    async def _queue_(self, ctx: commands.Context, url: str = parameter(description='- The YouTube URL that you would like ChetBot to play next')) -> None:

        # Checks that the unique directory exists that already contains the user's previous YouTube videos
        parent_dir = 'WorkingFiles/AudioFilesToUse/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        checkDirectoryExists(temp_directory)
        queued_song = f'{temp_directory}/{randomChar(10)}.mp3'

        await ctx.send(f'{ctx.author.mention}, your song is being processed...', delete_after=5)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(queued_song),
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        source = FFmpegPCMAudio(queued_song)
        guild_id = ctx.message.guild.id
        if guild_id in queues:
            queues[guild_id].append(source)
        else:
            queues[guild_id] = [source]

        await ctx.send(f'{ctx.author.mention}, your request has been added to the queue.', delete_after=5)

    # Pause file currently being played
    @_voice_.command(name='pause', with_app_command=True, description='Makes ChetBot pause the current audio.')
    @app_commands.guilds(495623660967690240)
    async def _pause_(self, ctx: commands.Context) -> None:
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send(f'I paused the audio.', delete_after=5)
        else:
            await ctx.send(f'{ctx.author.mention}, there is currently no audio being played.', delete_after=10)

    # Resume file currently paused
    @_voice_.command(name='resume', with_app_command=True, description='Makes ChetBot resume the paused audio.')
    @app_commands.guilds(495623660967690240)
    async def _resume_(self, ctx: commands.Context) -> None:
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send(f'I resumed playing the audio.', delete_after=5)
        else:
            await ctx.send(f'{ctx.author.mention}, there is currently no audio paused.', delete_after=10)

    # Stop file that is being played
    @_voice_.command(name='stop', with_app_command=True, description='Makes ChetBot cancel the current audio.')
    @app_commands.guilds(495623660967690240)
    async def _stop_(self, ctx: commands.Context) -> None:
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send(f'I stopped the audio from playing.', delete_after=5)

        # Removes the temp directory if music is stopped this way
        parent_dir = 'WorkingFiles/AudioFilesToUse/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        checkDirectoryExistsDelete(temp_directory)


async def setup(ChetBot):
    await ChetBot.add_cog(VoiceChannel(ChetBot))
