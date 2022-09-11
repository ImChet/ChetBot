import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from functions import check_queue, queues


class VoiceChannel(commands.Cog, name='Voice Channel Commands'):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # Join voice channel
    @commands.command(pass_context=True)
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.message.author.voice.channel.connect()
        else:
            await ctx.send(f'{ctx.author.mention}, you are not in a voice channel.', delete_after=5)

    # Leave voice channel
    @commands.command(pass_context=True)
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send(f'{ctx.author.mention}, I am not in a voice channel.', delete_after=5)

    # Play file located at arg
    @commands.command(pass_context=True)
    async def play(self, ctx, arg):
        if ctx.guild.voice_client is not None:
            voice = ctx.guild.voice_client
            source = FFmpegPCMAudio(arg)
            voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
        else:
            await ctx.send(f'{ctx.author.mention}, I am not in a voice channel.', delete_after=5)

    # Queues file located at arg to play next
    @commands.command(pass_context=True)
    async def queue(self, ctx, arg):
        source = FFmpegPCMAudio(arg)
        guild_id = ctx.message.guild.id
        if guild_id in queues:
            queues[guild_id].append(source)
        else:
            queues[guild_id] = [source]
        await ctx.send(f'{ctx.author.mention}, your request is added to the queue.', delete_after=5)

    # Pause file currently being played
    @commands.command(pass_context=True)
    async def pause(self, ctx):
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send(f'{ctx.author.mention}, there is currently no audio being played.', delete_after=5)

    # Resume file currently paused
    @commands.command(pass_context=True)
    async def resume(self, ctx):
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send(f'{ctx.author.mention}, there is currently no audio paused.', delete_after=5)

    # Stop file that is being played
    @commands.command(pass_context=True)
    async def stop(self, ctx):
        voice = discord.utils.get(self.ChetBot.voice_clients, guild=ctx.guild)
        voice.stop()


async def setup(ChetBot):
    await ChetBot.add_cog(VoiceChannel(ChetBot))
