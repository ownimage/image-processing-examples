import logging
import os
import re
import time

import rawpy
from PIL import Image

from xmp_processor import process
from captioner import Captioner

__extns = '(.+\.)(nef|NEF|jpg|JPG|dng|DNG)'
__captioner = Captioner()
__latest_directory = ''
__latest_directory_description = ''



def convert_image_name_to_xmp_name(image_name):
    if not re.match(__extns, image_name):
        return None
    return re.search(__extns, image_name).group(1) + 'xmp'


def image_file_with_xmp(filename, filenames):
    xmp_name = convert_image_name_to_xmp_name(filename)
    if xmp_name is None:
        return False
    return xmp_name in filenames


def get_directory_description(dir_path):
    __latest_directory_description = ''
    description_path = os.path.join(dir_path, 'description.txt')
    if os.path.isfile(description_path):
        file = open(description_path, 'r')
        description = file.read()
        file.close()
    return description


def get_image(image_path, size):
    raw = rawpy.imread(image_path)
    rgb = raw.postprocess()
    img = Image.fromarray(rgb)
    return img


def is_file_older_than(path, cutoff):
    b = os.path.getmtime(path) < cutoff
    logging.debug(f'is_file_older_than path: {path} result: {b}')
    return b


def describe_image(dirpath, image_filename, dir_description='', cutoff=time.time()):
    full_imagefilename = os.path.join(dirpath, image_filename)
    xmp_name = convert_image_name_to_xmp_name(full_imagefilename)
    if is_file_older_than(xmp_name, cutoff):
        process(xmp_name, 'ERROR ERRORERROR')
        image = get_image(full_imagefilename, 1024)
        logging.debug(f'image.width = {image.width}, image.height = {image.height}')
        description = dir_description
        description += '\n\n' + __captioner.describe(0, image)
        description += '\n\n' + __captioner.describe(1, image)
        description += '\n\n' + __captioner.describe(2, image)
        description += '\n\n' + __captioner.describe(4, image)
        description += '\n'
        logging.info(f'{xmp_name} : {description}\n')
        process(xmp_name, description)
        image.close()
        return description


def get_stats():
    return __captioner.get_stats()