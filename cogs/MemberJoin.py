import discord
from discord.ext import commands


class MemberJoin(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    # When member joins the guild, this gets called
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Welcome message embed
        string = f'Welcome to {member.guild.name}!\n'
        embed = discord.Embed(title=string)
        embed.set_thumbnail(url=member.guild.icon)
        await member.send(embed=embed)


async def setup(ChetBot):
    await ChetBot.add_cog(MemberJoin(ChetBot))
