from discord.ext import commands


class SlashSync(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        print('Todo')
        # Create command to sync manually not in main.py on startup


async def setup(ChetBot):
    await ChetBot.add_cog(SlashSync(ChetBot))
