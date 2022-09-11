# Steps needed to get ChetBot up and running

## Windows setup

### discord.py installation

##### Go to the directory where your ChetBot files have been downloaded, and in the terminal run the following:

`py -3 -m pip install -U discord.py`
`py -m pip install -U discord.py[voice]`

### You need FFmpeg

##### Go to: `https://ffmpeg.org/download.html#build-windows`

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

### You need FFmpeg

##### Steps:
* Open your Terminal, type the following: `sudo apt install ffmpeg`
* Check if FFmpeg is installed with the following: `FFmpeg -version`
* Restart your PC to ensure FFmpeg took effect