from datetime import datetime
from pdf2docx import Converter
import os

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


# Determines the method of which to convert files based on inputted type and desired type
def file_conversion(input_file, desired_outfile_type):
    # Supported file types
    pdf_file = ['.pdf']
    docx_file = ['.docx']
    jpeg_file = ['.jpeg', '.jpg']
    png_file = ['.png']

    # Need to get file extensions of the input files
    input_file_type = os.path.splitext(str(input_file)[1])
    input_file_name = os.path.splitext(str(input_file)[0])

    # Input conditional variable definitions
    input_is_pdf = input_file_type in pdf_file
    input_is_docx = input_file_type in docx_file
    input_is_jpeg = input_file_type in jpeg_file
    input_is_png = input_file_type in png_file

    # Output conditional variable definitions
    output_is_pdf = desired_outfile_type in pdf_file
    output_is_docx = desired_outfile_type in docx_file
    output_is_jpeg = desired_outfile_type in jpeg_file
    output_is_png = desired_outfile_type in png_file

    # .pdf to .docx
    if input_is_pdf and output_is_docx:
        # infile is .pdf
        infile = input_file
        outfile = (f'WorkingFiles/FilesToConvert/{input_file_name}')
        return
    # .docx to .pdf
    elif input_is_docx and output_is_pdf:
        return