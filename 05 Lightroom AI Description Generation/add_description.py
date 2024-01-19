import datetime
import logging
import os
import pprint
import sys
import time
from os import walk

from captioner import Captioner
from describe_image import describe_image, image_file_with_xmp, get_directory_description, get_stats

METHOD_COUNT = Captioner.get_method_count()
USAGE = 'python add_description.py <model_id> <directory_path>'
USAGE_MODEL_ID = f'model_id must be an integer >= 0 and < {METHOD_COUNT}.'
USAGE_FOLDER_HELP = 'the supplied <directory_path> does not exist.'

extns = '(.+\.)(nef|NEF|jpg|JPG|dng|DNG)'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
captioner = Captioner()

start_time = time.time()
start_time_string = datetime.datetime.now()
cutoff = start_time #- (3 * 60 * 60 * 24)


def print_usage():
    print(USAGE)
    print(USAGE_MODEL_ID)
    for i in range(METHOD_COUNT):
        print(f'{i}) - {captioner.describe(i, None)}')


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

w = walk(start_dirpath)
for (dirpath, dirnames, filenames) in w:
    dirnames.sort()
    image_filenames = [f for f in filenames if image_file_with_xmp(f, filenames)]
    dir_description = get_directory_description(dirpath)
    print(
        f'dirpath={dirpath} dirnames={dirnames} filenames={filenames} image_filenames={image_filenames} directory_description={dir_description}\n)')
    for image_filename in image_filenames:
        describe_image(dirpath, image_filename, dir_description, cutoff)
print('####################################################')
pprint.pprint(get_stats())
print(f'start_time: {start_time_string}')
print(f'  end_time: {datetime.datetime.now()}')
