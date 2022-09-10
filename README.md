# Windows 

### discord.py installation

`py -3 -m pip install -U discord.py`
`py -m pip install -U discord.py[voice]`

### Need FFmpeg

##### Go to: `https://ffmpeg.org/download.html#build-windows`

##### Steps:
* Extract the .exe
* Search "path" on Windows
* Go to "Edit the System Enviroment Variables"
* Click on "Enviroment Variables"
* Under System Variables double-click on "path"
* Click "new" and add file path containing the 3 .exe
* Click ok, and close out of everything
* Restart PC
* Make sure to import the module for FFmpeg: `from discord import FFmpegPCMAudio`

# Linux

### discord.py installation
`python3 -m pip install -U discord.py`
`python3 -m pip install -U discord.py[voice]`

### Need FFmpeg
`sudo apt install ffmpeg`

* Restart PC
* Make sure to import the module for FFmpeg: `from discord import FFmpegPCMAudio`