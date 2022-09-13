from datetime import datetime
from pdf2docx import parse
from docx2pdf import convert
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

    print(f'str(input_file) {str(input_file)}')  # test
    print(f'input_file_type {str(input_file_type)}')  # test
    print(f'input_file_name {str(input_file_name)}')  # test
    print(f'desired_outfile_type = {desired_outfile_type}')  # test

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

    print(f'input_is_docx = {input_is_docx}')  # testing
    print(f'output_is_pdf = {output_is_pdf}')  # testing

    # .pdf to .docx
    if input_is_pdf and output_is_docx:
        # infile is .pdf
        infile = input_file
        # outfile is .docx
        outfile = f'{input_file_name}{desired_outfile_type}'

        parse(infile, outfile)
        return outfile

    # .docx to .pdf
    elif input_is_docx and output_is_pdf:
        # infile is .docx
        infile = input_file
        # outfile is .pdf
        outfile = f'{input_file_name}{desired_outfile_type}'
        print(f'(in if) infile = {infile} and outfile = {outfile}')
        convert(infile, outfile)
        return outfile
