from urllib.parse import quote_plus

import discord
from discord import app_commands
from discord.ext import commands


class GoogleSearch(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query_passable = quote_plus(query)
        url = f'https://www.google.com/search?q={query_passable}'
        self.add_item(discord.ui.Button(label=f'Google Search for: {query}', url=url))


class GitHubSearch(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query_passable = quote_plus(query)
        url = f'https://github.com/search?q={query_passable}'
        self.add_item(discord.ui.Button(label=f'GitHub Search for: {query}', url=url))

class YouTubeSearch(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query_passable = quote_plus(query)
        url = f'https://www.youtube.com/results?search_query={query_passable}'
        self.add_item(discord.ui.Button(label=f'YouTube Search for: {query}', url=url))


class Views(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    @commands.hybrid_group(name='search', with_app_command=True,
                           description='Search for anything on your desired website.')
    async def _search_parent_command_(self, ctx: commands.Context):
        print('I am the parent search command')

    @_search_parent_command_.command(name='google', with_app_command=True,
                                     description='Search for anything you want to on Google.')
    @app_commands.describe(query='What you want to search for on Google')
    async def _google_search_(self, ctx: commands.Context, *, query: str):
        await ctx.reply(view=GoogleSearch(query))

    @_search_parent_command_.command(name='github', with_app_command=True,
                                     description='Search for anything you want to on GitHub.')
    @app_commands.describe(query='What you want to search for on GitHub')
    async def _github_search_(self, ctx: commands.Context, *, query: str):
        await ctx.reply(view=GitHubSearch(query))

    @_search_parent_command_.command(name='youtube', with_app_command=True,
                                     description='Search for anything you want to on YouTube.')
    @app_commands.describe(query='What you want to search for on YouTube')
    async def _github_search_(self, ctx: commands.Context, *, query: str):
        await ctx.reply(view=YouTubeSearch(query))


async def setup(ChetBot):
    await ChetBot.add_cog(Views(ChetBot))
