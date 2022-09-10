from datetime import datetime

# Variable Definitions
# Defining variables
queues = {}


# Function Definitions
# Current Datetime
def getDateTime():
    return f'{datetime.now().strftime("%m/%d/%Y")} at {(datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")).strftime("%r")}'


# To lowercase
def to_lower(arg):
    return arg.lower()


# To uppercase
def to_upper(arg):
    return arg.upper()


# Checks if the queue is populated and removes the current item in queue
def check_queue(ctx, arg):
    if queues[arg] != []:
        voice = ctx.guild.voice_client
        source = queues[arg].pop(0)
        voice.play(source)

