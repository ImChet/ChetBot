import discord
from discord import app_commands
from discord.ext import commands


class HelpButtonAdmin(discord.ui.View):
    def __init__(self):
        super().__init__()
        url = 'https://github.com/ImChet/ChetBot#administration-commands'
        self.add_item(discord.ui.Button(label='Administration Command Help', url=url))


class HelpButtonFile(discord.ui.View):
    def __init__(self):
        super().__init__()
        url = 'https://github.com/ImChet/ChetBot#file-commands'
        self.add_item(discord.ui.Button(label='File Operation Command Help', url=url))


class HelpButtonRole(discord.ui.View):
    def __init__(self):
        super().__init__()
        url = 'https://github.com/ImChet/ChetBot#role-commands'
        self.add_item(discord.ui.Button(label='Role Command Help', url=url))


class HelpButtonVoice(discord.ui.View):
    def __init__(self):
        super().__init__()
        url = 'https://github.com/ImChet/ChetBot#voice-channel-commands'
        self.add_item(discord.ui.Button(label='Voice Channel Command Help', url=url))


class HelpButtonMisc(discord.ui.View):
    def __init__(self):
        super().__init__()
        url = 'https://github.com/ImChet/ChetBot#miscellaneous-commands'
        self.add_item(discord.ui.Button(label='Miscellaneous Command Help', url=url))


class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Administration Commands', description='You need help with Administration Commands'),
            discord.SelectOption(label='File Operation Commands', description='You need help with File Operation Commands'),
            discord.SelectOption(label='Role Commands', description='You need help with Role Commands'),
            discord.SelectOption(label='Voice Channel Commands', description='You need help with Voice Channel Commands'),
            discord.SelectOption(label='Miscellaneous Commands', description='You need help with Miscellaneous Commands')
        ]
        super().__init__(placeholder='Pick what topic you need help with...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values == ['Administration Commands']:
            await interaction.response.send_message(view=HelpButtonAdmin())
        elif self.values == ['File Operation Commands']:
            await interaction.response.send_message(view=HelpButtonFile())
        elif self.values == ['Role Commands']:
            await interaction.response.send_message(view=HelpButtonRole())
        elif self.values == ['Voice Channel Commands']:
            await interaction.response.send_message(view=HelpButtonVoice())
        elif self.values == ['Miscellaneous Commands']:
            await interaction.response.send_message(view=HelpButtonMisc())


class HelpDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpDropdown())


class Help(commands.Cog):

    def __init__(self, ChetBot):
        self.ChetBot = ChetBot

    @app_commands.command(name='help', description='If you need assistance with anything related to ChetBot.')
    @app_commands.guilds(495623660967690240)
    async def _help_(self, interaction: discord.Interaction):
        view = HelpDropdownView()
        await interaction.response.send_message(view=view)


async def setup(ChetBot):
    await ChetBot.add_cog(Help(ChetBot))
