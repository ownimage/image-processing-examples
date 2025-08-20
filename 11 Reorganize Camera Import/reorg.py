import os
import platform
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime


def reorg(directory):
    # loop over files in directory
    for filename in os.listdir(directory):
        # join path and filename
        path = os.path.join(directory, filename)
        print(filename)

        # check if path is a file
        if os.path.isfile(path) and is_image(path):
            # extract file extension
            ymd = extract_file_create_date(path)

            # create new directory if it doesn't exist
            new_dir = os.path.join(directory, ymd)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            if is_jpg(path):
                new_dir = os.path.join(directory, ymd, 'origJPG')
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
                new_path = os.path.join(new_dir, filename)
                os.rename(path, new_path)
            else:
                new_path = os.path.join(new_dir, filename)
                os.rename(path, new_path)

    print("Files organized successfully.")


def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension


def is_image(file_path):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.nef'}
    return get_file_extension(file_path).lower() in image_extensions


def is_jpg(file_path):
    image_extensions = {'.jpg', '.jpeg'}
    return get_file_extension(file_path).lower() in image_extensions


def extract_file_create_date(image_path):
    image = Image.open(image_path)
    exif_data = image.getexif()

    if not exif_data:
        return None

    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 'DateTime':
            # Format is usually 'YYYY:MM:DD HH:MM:SS'
            date_taken = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
            return date_taken.strftime('%Y%m%d')

    return None

if __name__ == '__main__':
    directory = sys.argv[1]
    print(directory)
    reorg(directory)
