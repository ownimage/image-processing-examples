import os
import pathlib
import sys

from captioner import Captioner

METHOD_COUNT = Captioner.get_method_count()
USAGE = 'python add_description.py <model_id> <directory_path>'
USAGE_MODEL_ID = f'model_id must be an integer >= 0 and < {METHOD_COUNT}.'
USAGE_FOLDER_HELP = 'the supplied <directory_path> does not exist.'

IMAGE_EXTNS = ['.NEF', '.JPG', '.DNG']

if len(sys.argv) != 3:
    print(USAGE)
    exit()

try:
    model_id = int(sys.argv[1])
    if 0 <= model_id < METHOD_COUNT:
        print(f'model_id = {model_id}')
    else:
        exit()
except:
    print(USAGE)
    print(USAGE_MODEL_ID)
    exit()

dir_path = sys.argv[2]
print(f'directory_path = {dir_path}')
if not os.path.isdir(dir_path):
    print(USAGE)
    print(USAGE_FOLDER_HELP)
    exit()

captioner = Captioner(model_id)

# file = 'F:/Keith/04. Photos/20150514 ColorChecker/20170329/DSC_0126-198.dng'
# print(f'{file} : {captioner.describe(file)}')

for path in os.listdir(dir_path):
    file = os.path.join(dir_path, path)
    if os.path.isfile(file):
        path = pathlib.Path(path)
        if path.suffix.upper() in IMAGE_EXTNS:
            print(f'{file} : {captioner.describe(file)}')

