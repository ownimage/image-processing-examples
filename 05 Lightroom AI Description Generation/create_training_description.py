import logging
import os
import re
import sys

from captioner import Captioner
from image_util import get_image

METHOD_COUNT = Captioner.get_method_count()
USAGE = 'python create_training_description.py <model_id>(,model_id)* <directory_path>'
USAGE_MODEL_ID = f'model_id must be an integer >= 0 and < {METHOD_COUNT}.'
USAGE_FOLDER_HELP = 'the supplied <directory_path> does not exist.'
SEPARATOR_LINE = '##########################'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
captioner = Captioner()


class CreateTrainingDescriptions:
    def __init__(self):
        self.__extns = '(.+\.)(nef|NEF|dng|DNG|tiff|TIFF|tif|TIF|jpg|JPG|jpeg|JPEG)'

    def filename_has_image_ext(self, filename):
        return re.match(self.__extns, filename) is not None

    def convert_image_filename_to_txt(self, filename):
        if not self.filename_has_image_ext(filename):
            return None
        return re.search(self.__extns, filename).group(1) + 'txt'


def print_usage():
    print(USAGE)
    print(USAGE_MODEL_ID)
    for i in range(METHOD_COUNT):
        print(f'{i}) - {captioner.describe(i, None)}')


if len(sys.argv) != 3:
    print_usage()
    exit()

try:
    model_ids = list(map(lambda m: int(m), sys.argv[1].split(',')))
    for model_id in model_ids:
        if model_id >= METHOD_COUNT:
            message = f'Invalid model_id: {model_id}'
            print(message)
            raise Exception(message)

except:
    print_usage()
    exit()

directory = sys.argv[2]
print(f'directory_path = {directory}')
if not os.path.isdir(directory):
    print_usage()
    print(USAGE_FOLDER_HELP)
    exit()

print(f'\n\n\n{SEPARATOR_LINE}\nmodel_ids = {model_ids}\ndirectory = {directory}\n{SEPARATOR_LINE}')

createTrainingDescriptions = CreateTrainingDescriptions()
images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
images = list(filter(lambda f: createTrainingDescriptions.filename_has_image_ext(f), images))
print(images)

for i in images:
    print(i)
    t = createTrainingDescriptions.convert_image_filename_to_txt(i)
    f = open(os.path.join(directory, t), 'w')
    image = get_image(os.path.join(directory, i))
    for m in model_ids:
        d = captioner.describe(m, image)
        f.write(f'{d}\n')
    f.close()
