import os
import sys
import logging
from PIL import Image
from os import walk
import re
from xmp_processor import process

from captioner import Captioner

METHOD_COUNT = Captioner.get_method_count()
USAGE = 'python add_description.py <model_id> <directory_path>'
USAGE_MODEL_ID = f'model_id must be an integer >= 0 and < {METHOD_COUNT}.'
USAGE_FOLDER_HELP = 'the supplied <directory_path> does not exist.'

extns = '(.+\.)(nef|NEF|jpg|JPG|dng|DNG)'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
captioner = Captioner()


def print_usage():
    print(USAGE)
    print(USAGE_MODEL_ID)
    for i in range(METHOD_COUNT):
        print(f'{i}) - {captioner.describe(i, None)}')


def convert_image_name_to_xmp_name(image_name):
    if not re.match(extns, image_name):
        return None
    return re.search(extns, image_name).group(1) + 'xmp'


def image_file_with_xmp(filename, filenames):
    xmp_name = convert_image_name_to_xmp_name(filename)
    if xmp_name is None:
        return False
    return xmp_name in filenames


if len(sys.argv) != 3:
    print_usage()
    exit()

try:
    model_id = int(sys.argv[1])
    if 0 <= model_id < METHOD_COUNT:
        print(f'model_id = {model_id}')
    else:
        exit()
except:
    print_usage()
    exit()


def get_directory_description(dir_path):
    description = ''
    description_path = os.path.join(dir_path, 'description.txt')
    if os.path.isfile(description_path):
        file = open(description_path, 'r')
        description = file.read()
        file.close()
    return description


start_dirpath = sys.argv[2]
print(f'directory_path = {start_dirpath}')
if not os.path.isdir(start_dirpath):
    print_usage()
    print(USAGE_FOLDER_HELP)
    exit()

w = walk(start_dirpath)
for (dirpath, dirnames, filenames) in w:
    image_filenames = [f for f in filenames if image_file_with_xmp(f, filenames)]
    dir_description = get_directory_description(dirpath)
    print(f'dirpath={dirpath} dirnames={dirnames} filenames={filenames} image_filenames={image_filenames} directory_description={dir_description}\n)')
    for image_filename in image_filenames:
        full_imagefilename = os.path.join(dirpath, image_filename)
        full_imagefile = open(full_imagefilename, 'rb')
        image = Image.open(full_imagefile)
        description = dir_description
        description += '\n\n' + captioner.describe(0, image)
        description += '\n\n' + captioner.describe(1, image)
        description += '\n\n' + captioner.describe(2, image)
        description += '\n'
        xmp_name = convert_image_name_to_xmp_name(full_imagefilename)
        print(f'{xmp_name} : {description}\n')
        process(xmp_name, description)
        image.close()
        full_imagefile.close()
print(f'####################################################\n{captioner.get_stats()}')
