import os
from datetime import datetime

from PIL import Image
from docx2pdf import convert
from pdf2docx import parse

# Variable Definitions
# Defining variables
queues = {}


# Function Definitions
# Current Datetime
def getCurrentDateTime():
    return f'{datetime.now().strftime("%m/%d/%Y")} at {(datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")).strftime("%r")}'


# Current Time
def getTime(chosenDelimiter: str):
    output = f'%I{chosenDelimiter}%M{chosenDelimiter}%S'
    return f'{datetime.now().strftime(output)}'


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
    # Set desired_outfile_type to include '.'
    desired_outfile_type = f'.{desired_outfile_type}'

    # Supported file types
    pdf_file = ['.pdf']
    docx_file = ['.docx']
    jpeg_file = ['.jpeg', '.jpg']
    png_file = ['.png']

    # Need to get file extensions of the input files
    input_file_type = (os.path.splitext(str(input_file))[1])
    input_file_name = (os.path.splitext(str(input_file))[0])

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

    # .pdf to .docx (utilizes pdf2docx.parse)
    if input_is_pdf and output_is_docx:
        # infile is .pdf
        infile = input_file
        # outfile is .docx
        outfile = f'{input_file_name}{desired_outfile_type}'
        parse(infile, outfile)
        return outfile

    # .docx to .pdf (utilizes docx2pdf.convert)
    elif input_is_docx and output_is_pdf:
        # infile is .docx
        infile = input_file
        # outfile is .pdf
        outfile = f'{input_file_name}{desired_outfile_type}'
        convert(infile, outfile)
        return outfile

    # .jpeg to .pdf (utilizes PIL.Image)
    elif input_is_jpeg and output_is_pdf:
        # infile is .jpeg
        infile = Image.open(input_file)
        # outfile is .pdf
        outfile_path = f'{input_file_name}{desired_outfile_type}'
        outfile = infile.convert('RGB')
        outfile.save(outfile_path)
        return outfile_path

    elif input_is_png and output_is_pdf:
        # infile is .png
        infile = Image.open(input_file)
        # outfile is .pdf
        outfile_path = f'{input_file_name}{desired_outfile_type}'
        outfile = infile.convert('RGB')
        outfile.save(outfile_path)
        return outfile_path

    elif input_is_png and output_is_jpeg:
        # infile is .png
        infile = Image.open(input_file)
        # outfile is .jpeg
        outfile_path = f'{input_file_name}{desired_outfile_type}'
        outfile = infile.convert('RGB')
        outfile.save(outfile_path)
        return outfile_path

    else:
        not_supported = None
        return not_supported
