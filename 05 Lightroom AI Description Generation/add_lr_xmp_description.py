import datetime
import logging
import os
import pprint
import sys
import time
from os import walk

from captioner import Captioner
from describe_image import Describe_Image
from slack_notifier import SlackNotifier
from timestamp_properties import get_timestamp

METHOD_COUNT = Captioner.get_method_count()
USAGE = 'python add_description.py <model_id> <directory_path>'
USAGE_MODEL_ID = f'model_id must be an integer >= 0 and < {METHOD_COUNT}.'
USAGE_FOLDER_HELP = 'the supplied <directory_path> does not exist.'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
captioner = Captioner()
describe_image = Describe_Image()

start_time = time.time()
start_time_string = datetime.datetime.now()
cutoff = float(get_timestamp('run.properties', 'start'))


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

slack_notifier = SlackNotifier()
slack_notifier.send_notification('Starting', 'summary')


def image_file_with_xmp_older_than(path: str, filename: str, filenames: [str]):
    """
    Parameters
    ----------
    path: str
        The directory that the filename and filenames are in.

    filename: str
        The name of a candidate image file.

    filenames: [str]
        All the filenames in the directory.

    checks that the filename give is a valid image file and it exists
    and that the associated .xmp file is in the list of filenames

    """
    return describe_image.image_file_with_xmp_older_than(path, filename, filenames, cutoff)


class Counter:
    def __init__(self):
        self.__count = 0

    def filter(self, path, filename, filenames):
        return image_file_with_xmp_older_than(path, filename, filenames)

    def process(self, dirpath, image_filename):
        self.__count += 1

    def count(self):
        return self.__count


class Processor:
    def __init__(self, total):
        self.__TOTAL_IMAGES = total
        self.__count = 0
        self.__total_time = 0
        self.__previous_time = 0

    def filter(self, path, filename, filenames):
        return image_file_with_xmp_older_than(path, filename, filenames)

    def process(self, dirpath, image_filename):
        now = time.time()
        if self.__count != 0:
            self.__total_time += (now - self.__previous_time)
        self.__previous_time = now
        self.__count += 1
        print(f'image {self.__count} of {self.__TOTAL_IMAGES} {dirpath}\\{image_filename}')
        description = describe_image.describe_image(dirpath, image_filename)
        if description is not None:
            remaining = self.estimate_remaining()
            full_image_filename = os.path.join(dirpath, image_filename)
            message = f'image {self.__count} of {self.__TOTAL_IMAGES}  {remaining}    {full_image_filename}    {description}'
            slack_notifier.send_notification_with_image(message, dirpath, image_filename, 'feed')

    def estimate_remaining(self):
        if self.__count != 0:
            average_time = self.__total_time / self.__count
            print(f'average_time = {average_time}')
            remaining_time = (self.__TOTAL_IMAGES - self.__count) * average_time

            days = remaining_time // (24 * 60 * 60)
            seconds = remaining_time % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            print("%d:%d:%02d:%02d" % (days, hour, minutes, seconds))
            return f'{days} days {hour} hours {minutes} minutes remaining.'


def walk_and_do(start_dirpath, processor):
    w = walk(start_dirpath)
    for (dirpath, dirnames, filenames) in w:
        dirnames.sort()
        filenames.sort()
        image_filenames = [filename for filename in filenames if processor.filter(dirpath, filename, filenames)]
        for image_filename in image_filenames:
            processor.process(dirpath, image_filename)
            if os.path.exists("stop"):
                exit()


counter = Counter()
walk_and_do(start_dirpath, counter)
processor = Processor(counter.count())
walk_and_do(start_dirpath, processor)
slack_notifier.send_notification(f'Ending: {describe_image.get_stats()}', 'summary')
