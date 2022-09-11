# Steps needed to get ChetBot up and running

## Windows setup

### discord.py installation

##### Go to the directory where your ChetBot files have been downloaded, and in the terminal run the following:

`py -3 -m pip install -U discord.py`
`py -m pip install -U discord.py[voice]`

### FFmpeg installation

FFmpeg download: `https://ffmpeg.org/download.html#build-windows`

##### Steps:
* Extract the .exe files from the .zip file
* Search "path" in the Windows search
* Go to "Edit the System Enviroment Variables"
* Click on "Enviroment Variables"
* Under System Variables double-click on "Path"
* Click "new" and add the file path containing the 3x .exe files extracted
* Click ok, and close out of everything
* Navigate to your cmd, check if FFmpeg is installed with the following: `FFmpeg -version`
* Restart your PC to ensure FFmpeg took effect
* Make sure to import the module for FFmpeg: `from discord import FFmpegPCMAudio`

## Linux setup

### discord.py installation

##### Go to the directory where your ChetBot files have been downloaded, and in the terminal run the following:

`python3 -m pip install -U discord.py`
`python3 -m pip install -U discord.py[voice]`

### FFmpeg installation

##### Steps:
* Open your Terminal, type the following: `sudo apt install ffmpeg`
* Check if FFmpeg is installed with the following: `FFmpeg -version`
* Restart your PC to ensure FFmpeg took effect

# Creating your own Discord Bot

If you wish to create your own Discord Bot, it needs to work with the discord.py library and the Discord API. 

### Making a Discord Bot account

##### Steps:
* Navigate to: `https://discord.com/developers/applications`
* Click on the "New Application"
* Give your application a name and click "Create"
* Next, create a Bot User by navigating to the tab labeled "Bot", and clicking "Add Bot"
  * Click "Yes, do it" to continue
* If you want your Bot to be able ot join other people's servers, you must ensure that the option "Public Bot" is checked
  * Also, make sure that the option "Require OAuth2 Code Grant" is unchecked unless you are working with or developing a service that needs it.
* Generate your Bot's API Key and copy it

Now that you have that API Key, you can use your program to login to Discord with your new Bot account.

### Inviting your Discord Bot account

So you made your new Bot, but it is not in any server yet. Here are the steps to invite it to any server of your choosing (Assuming you have permission to invite users).

Firstly, you must create an invite URL for your bot.
##### Steps:
* Navigate to: `https://discord.com/developers/applications`
* Click on your Bot's page
* Go to the "OAuth2" tab on the left-hand side
  * Then navigate to the sub-option "OAuth2 URL Generator"
* Tick the "bot" scope checkbox
  * A new list of checkbox options should appear under the scopes section called "Bot Permissions"
* Under this new section, check the boxes matching the permissions that your bot will require when it joins a server to function as intended
  * Make sure that you are aware of the consequences of requiring your bot to have the “Administrator” permission
* The resulting URL that is generated at the bottom of the screen can be copied when all of the required permissions for your Bot have been checked
* Paste the URL into your web browser and choose which server you would like to have your Bot join, and click "Authorize"

Your Bot should now have successfully joined the Discord Server of your choosing.

### Working with your Discord Bot

Now that you have generated your Discord Bot's API Key and you have invited it to the server(s) of your choosing, you probably want to get to work making your Bot function as you wish.

To do this, make sure that you have cloned the ChetBot files from my GitHub.
##### Steps:
* Follow the instructions on the [GitHub docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) if you are unfamiliar with cloning repositories
  * ChetBot repository Link: `https://github.com/ImChet/ChetBot.git`
* In the newly cloned ChetBot repository, find the apikeys.py file, navigate to the discordBotAPIKey function and place your Discord Bot API Key in the return statement 

You are now ready to use your Discord Bot. 

To do this, run the main.py file to sign onto Discord as your Bot.

You may use the built-in ChetBot commands and event listeners as examples for your own Bot.