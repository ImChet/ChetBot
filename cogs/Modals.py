import discord
from discord import app_commands
from discord.ext import commands

from functions import getCurrentDateTime


# Modals can only have text
class Feedback(discord.ui.Modal, title='Feedback on ChetBot'):
    name = discord.ui.TextInput(
        label='Name',
        placeholder='Enter your name here...',
        required=True
    )
    feedback = discord.ui.TextInput(
        label='What feedback do you have?',
        style=discord.TextStyle.paragraph,
        placeholder='Type your feedback here...',
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f'Thank you for submitting your feedback, {interaction.user.mention}!',
                                                ephemeral=True)
        working_file = f'ChetBot_Feedback.txt'
        f = open(working_file, "a")
        f.write(f'-----\nFrom: {str(self.name.value)}\n'
                f'Discord Name:{str(interaction.user.name)}#{str(interaction.user.discriminator)}\n'
                f'Feedback: {str(self.feedback.value)}\n'
                f'Time feedback sent: on {getCurrentDateTime()}\n'
                f'-----\n')
        f.close()


class Modals(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    @app_commands.command(name='feedback', description='Submit feedback to the creator of ChetBot.')
    async def _feedback_modal_(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Feedback())


async def setup(ChetBot):
    await ChetBot.add_cog(Modals(ChetBot))
