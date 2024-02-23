from os import walk
import re

extns = '(.+\.)(nef|NEF|jpg|JPG|dng|DNG)'


def convert_image_name_to_xmp_name(image_name):
    if not re.match(extns, image_name):
        return None
    return re.search(extns, image_name).group(1) + 'xmp'


def image_file_with_xmp(filename, filenames):
    xmp_name = convert_image_name_to_xmp_name(filename)
    if xmp_name is None:
        return False
    return xmp_name in filenames


print(f"xmp_name = {convert_image_name_to_xmp_name('parrot.jpg')}")

w = walk("test")
for (dirpath, dirnames, filenames) in w:
    image_filenames = [f for f in filenames if image_file_with_xmp(f, filenames)]
    print(f'dirpath={dirpath} dirnames={dirnames} filenames={filenames} image_filenames={image_filenames})')
