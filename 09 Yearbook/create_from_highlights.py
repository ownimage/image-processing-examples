import os
import os.path
import sys
from pathlib import Path
import shutil


def create(yearbook_dir, dir_name):
    process_dir(yearbook_dir, Path(dir_name))


def process_dir(yearbook_dir, dir):
    print(f'Processing {dir}')
    dirname = os.path.split(dir)[1]
    print(f'dirname = {dirname}')
    for subdir in [f for f in dir.iterdir() if f.is_dir()]:
        print(f"subdir = {subdir}")
        os.system(f'copy "P:\\git\\image-processing-examples\\08c Slideshow Python and Photoshop\\bootstrap.cmd" "{subdir}"')
        os.chdir(subdir)
        os.system("bootstrap.cmd")


# def process_slideshow(yearbook_dir, dir_name):
#     print(f'### Processing Slideshow {dir_name} to {yearbook_dir}')
#     prefix = os.path.basename(os.path.split(dir_name)[0])[0:8] + '_'
#     print(f'prefix = {prefix}')
#     for file in dir_name.glob("*.jpg"):
#         print(f'### ### {file.name}')
#         shutil.copyfile(os.path.join(dir_name, file.name), os.path.join(yearbook_dir, prefix + file.name))


dir_name = sys.argv[1]
yearbook_dir = os.path.join(dir_name, 'yearbook')

create(yearbook_dir, dir_name)
