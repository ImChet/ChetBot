import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import parameter

from functions import check_queue, queues


class VoiceChannel(commands.Cog, name='Voice Channel Commands', description='Voice Channel Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Join voice channel
    @commands.command(name='join', description='Makes ChetBot join the Voice Channel that you are currently in.\n---------------\n/join')
    async def _join_(self, ctx):
        if ctx.author.voice:
            await ctx.message.author.voice.channel.connect()
        else:
            await ctx.send(f'{ctx.author.mention}, you are not in a voice channel.', delete_after=5)

    # Leave voice channel
    @commands.command(name='leave', description='Makes ChetBot leave the Voice Channel that you are currently in.\n---------------\n/leave')
    async def _leave_(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send(f'{ctx.author.mention}, I am not in a voice channel.', delete_after=5)

    # Play file located at audio
    @commands.command(name='play', description='Makes ChetBot play audio.\n---------------\n/play <audio>')
    async def _play_(self, ctx, audio: str = parameter(description='- The audio that you would like ChetBot to play')):
        if ctx.guild.voice_client is not None:
            voice = ctx.guild.voice_client
            source = FFmpegPCMAudio(audio)
            voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
        else:
            await ctx.send(f'{ctx.author.mention}, I am not in a voice channel.', delete_after=5)

    # Queues file located at audio to play next
    @commands.command(name='queue', description='Makes ChetBot queue audio to play next.\n---------------\n/queue <audio>')
    async def _queue_(self, ctx, audio: str = parameter(description='- The audio that you would like ChetBot to play next')):
        source = FFmpegPCMAudio(audio)
        guild_id = ctx.message.guild.id
        if guild_id in queues:
            queues[guild_id].append(source)
        else:
            queues[guild_id] = [source]
        await ctx.send(f'{ctx.author.mention}, your request is added to the queue.', delete_after=5)

    # Pause file currently being played
    @commands.command(name='pause', description='Makes ChetBot pause the current audio.\n---------------\n/pause')
    async def _pause_(self, ctx):
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send(f'{ctx.author.mention}, there is currently no audio being played.', delete_after=5)

    # Resume file currently paused
    @commands.command(name='resume', description='Makes ChetBot resume the paused audio.\n---------------\n/resume')
    async def _resume_(self, ctx):
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send(f'{ctx.author.mention}, there is currently no audio paused.', delete_after=5)

    # Stop file that is being played
    @commands.command(name='stop', description='Makes ChetBot cancel the current audio.\n---------------\n/stop')
    async def _stop_(self, ctx):
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        voice.stop()


async def setup(ChetBot):
    await ChetBot.add_cog(VoiceChannel(ChetBot))
