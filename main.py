import asyncio
import logging.handlers
import os

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand

from apikeys import discordBotAPIKey
from functions import checkDirectoryExists


# ChetBot constructor class
class CreateBot(commands.Bot):
    def __init__(self):
        # Specifies intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True
        super().__init__(command_prefix="/", intents=intents,
                         help_command=None,
                         activity=discord.Activity(type=discord.ActivityType.watching, name='over the universe'),
                         status=discord.Status.do_not_disturb)

    async def setup_hook(self) -> None:
        print("ChetBot spinning up...\n-----")
        # REMOVE WHEN GOING GLOBAL
        await self.tree.sync(guild=discord.Object(id=495623660967690240))
        print("Slash commands synced. Proceeding...\n-----")


ChetBot = CreateBot()

# Defines the initial_extensions array
initial_extensions = []

# Logging setup / parameters
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logHandler = logging.FileHandler(filename='ChetBot.log', encoding='utf-8', mode='w')
loggingDateFormat = '%Y-%m-%d %H:%M:%S'
loggingFormatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', loggingDateFormat, style='{')
logHandler.setFormatter(loggingFormatter)
logger.addHandler(logHandler)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append('cogs.' + filename[:-3])


async def main():
    # Ensures the all the needed working directories exist
    checkDirectoryExists('WorkingFiles/')
    checkDirectoryExists('WorkingFiles/FilesToCreate/')
    checkDirectoryExists('WorkingFiles/FilesToConvert/')
    checkDirectoryExists('WorkingFiles/FilesToCombine/')
    checkDirectoryExists('WorkingFiles/AudioFilesToUse/')
    checkDirectoryExists('WorkingFiles/FilesToUpload/')

    # Loads all cogs
    for extension in initial_extensions:
        await ChetBot.load_extension(extension)


# Context menus are not supported in group contexts (cogs)
@ChetBot.tree.context_menu(name='Summon')
@app_commands.guilds(495623660967690240)
async def summon_context_menu(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f'{member.mention} has been summoned by {interaction.user.mention}')


if __name__ == '__main__':
    asyncio.run(main())

ChetBot.run(discordBotAPIKey, log_handler=None)
