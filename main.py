import asyncio
import os

import logging.handlers
import discord
from discord.ext import commands

from apikeys import discordBotAPIKey
from functions import getCurrentDateTime

# Specifies intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

# Creates the client connection to Discord and sets command prefix
ChetBot = commands.Bot(command_prefix="/", intents=intents)

# Defines the initial_extensions array
initial_extensions = []


# on_ready is called when the Bot has logged on/set things up and sets the bot status
@ChetBot.event
async def on_ready():
    await ChetBot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name='over the universe'))
    print(f'We have logged in as {ChetBot.user} on {getCurrentDateTime()}')

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
    for extension in initial_extensions:
        await ChetBot.load_extension(extension)

if __name__ == '__main__':
    asyncio.run(main())

ChetBot.run(discordBotAPIKey, log_handler=None)
