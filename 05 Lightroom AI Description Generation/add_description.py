import os
import pathlib
import sys
import logging
from PIL import Image
from os import walk
import re

from captioner import Captioner

METHOD_COUNT = Captioner.get_method_count()
USAGE = 'python add_description.py <model_id> <directory_path>'
USAGE_MODEL_ID = f'model_id must be an integer >= 0 and < {METHOD_COUNT}.'
USAGE_FOLDER_HELP = 'the supplied <directory_path> does not exist.'

extns = '(.+\.)(nef|NEF|jpg|JPG|dng|DNG)'


def print_usage():
    print(USAGE)
    print(USAGE_MODEL_ID)
    for i in range(METHOD_COUNT):
        print(f'{i}) - model name')


def convert_image_name_to_xmp_name(image_name):
    if not re.match(extns, image_name):
        return None
    return re.search(extns, image_name).group(1) + 'xmp'


def image_file_with_xmp(filename, filenames):
    xmp_name = convert_image_name_to_xmp_name(filename)
    if xmp_name is None:
        return False
    return xmp_name in filenames


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
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

start_dirpath = sys.argv[2]
print(f'directory_path = {start_dirpath}')
if not os.path.isdir(start_dirpath):
    print_usage()
    print(USAGE_FOLDER_HELP)
    exit()

captioner = Captioner()

# file = 'F:/Keith/04. Photos/20150514 ColorChecker/20170329/DSC_0126-198.dng'
# print(f'{file} : {captioner.describe(file)}')

w = walk("test")
for (dirpath, dirnames, filenames) in w:
    image_filenames = [f for f in filenames if image_file_with_xmp(f, filenames)]
    print(f'dirpath={dirpath} dirnames={dirnames} filenames={filenames} image_filenames={image_filenames})')
    for image_filename in image_filenames:
        full_imagefile = open(os.path.join(dirpath, image_filename), 'rb')
        image = Image.open(full_imagefile)
        print(f'{image_filename} : {captioner.describe(model_id, image)}')
        image.close()
        full_imagefile.close()


