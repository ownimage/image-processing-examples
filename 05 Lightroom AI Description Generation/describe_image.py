import logging
import os
import re
import time

from captioner import Captioner
from xmp_processor import process
from image_util import get_image


class Describe_Image:

    def __init__(self):
        self.__extns = '(.+\.)(nef|NEF|dng|DNG|tiff|TIFF|tif|TIF)'
        self.__captioner = Captioner()
        self.__latest_directory = ''
        self.__latest_directory_description = ''

    def convert_image_name_to_xmp_name(self, image_name):
        if not re.match(self.__extns, image_name):
            return None
        return re.search(self.__extns, image_name).group(1) + 'xmp'

    def image_file_with_xmp_older_than(self, path, filename, filenames, cutoff=time.time()):
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
        xmp_name = self.convert_image_name_to_xmp_name(filename)
        if xmp_name is None or not self.is_file_older_than(os.path.join(path, xmp_name), cutoff):
            return False
        return xmp_name in filenames

    def get_directory_description(self, dir_path):
        if self.__latest_directory != dir_path:
            self.__latest_directory = dir_path
            self.__latest_directory_description = ''
            description_path = os.path.join(dir_path, 'description.txt')
            if os.path.isfile(description_path):
                file = open(description_path, 'r')
                self.__latest_directory_description = file.read()
                file.close()
        return self.__latest_directory_description

    def is_file_older_than(self, path, cutoff):
        b = os.path.isfile(path) and os.path.getmtime(path) < cutoff
        logging.debug(f'is_file_older_than path: {path} result: {b}')
        return b

    def describe_image(self, dirpath, image_filename, dir_description='', size=0):
        full_imagefilename = os.path.join(dirpath, image_filename)
        xmp_name = self.convert_image_name_to_xmp_name(full_imagefilename)
        process(xmp_name, 'ERROR ERRORERROR')
        image = get_image(full_imagefilename, size)
        logging.debug(f'image.width = {image.width}, image.height = {image.height}')
        description = dir_description
        description += '\n\n' + self.__captioner.describe(0, image)
        description += '\n\n' + self.__captioner.describe(1, image)
        description += '\n\n' + self.__captioner.describe(2, image)
        description += '\n\n' + self.__captioner.describe(4, image)
        description += '\n'
        logging.info(f'{xmp_name} : {description}\n')
        process(xmp_name, description)
        image.close()
        return description

    def get_stats(self):
        return self.__captioner.get_stats()
