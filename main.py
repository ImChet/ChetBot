import asyncio
import os

import logging.handlers
import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand

from apikeys import discordBotAPIKey


# ChetBot constructor class
class CreateBot(commands.Bot):
    def __init__(self):
        # Specifies intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True
        super().__init__(command_prefix="/", intents=intents, help_command=DefaultHelpCommand(no_category='Help Command'), activity=discord.Activity(type=discord.ActivityType.watching, name='over the universe'), status=discord.Status.do_not_disturb)

    async def setup_hook(self) -> None:
        # remove this when syncing globally
        # avoid ratelimiting
        # guild=discord.Object(id=495623660967690240)
        await self.tree.sync(guild=discord.Object(id=495623660967690240))
        print(f'Synced slash commands.')


ChetBot = CreateBot()

# Defines the initial_extensions array
initial_extensions = []

# Logging setup / parameters
logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
logHandler = logging.FileHandler(filename='ChetBot.log', encoding='utf-8', mode='w')
loggingDateFormat = '%Y-%m-%d %H:%M:%S'
loggingFormatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', loggingDateFormat, style='{')
logHandler.setFormatter(loggingFormatter)
logger.addHandler(logHandler)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append('cogs.' + filename[:-3])


async def main():
    # Ensures the WorkingFiles directory exists
    path = 'WorkingFiles/'
    directory_exists = os.path.exists(path)
    if directory_exists is False:
        os.mkdir(path)
    # Loads all cogs
    for extension in initial_extensions:
        await ChetBot.load_extension(extension)

if __name__ == '__main__':
    asyncio.run(main())

ChetBot.run(discordBotAPIKey, log_handler=None)
