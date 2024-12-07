import os
import os.path
import sys
from pathlib import Path
import shutil


def yearbook(yearbook_dir, dir_name):
    process_dir(yearbook_dir, Path(dir_name), 0)


def process_dir(yearbook_dir, dir, level):
    print(f'Processing {dir}, level={level}')
    dirname = os.path.split(dir)[1]
    # print(f'dirname = {dirname}')

    if dirname == 'slideshow':
        process_slideshow(yearbook_dir, dir)
    else:
        if level < 3:
            for subdir in [f for f in dir.iterdir() if f.is_dir()]:
                process_dir(yearbook_dir, subdir, level + 1)


def process_slideshow(yearbook_dir, dir_name):
    print(f'### Processing Slideshow {dir_name} to {yearbook_dir}')
    prefix = os.path.basename(os.path.split(dir_name)[0])[0:8] + '_'
    print(f'prefix = {prefix}')
    for file in dir_name.glob("*.jpg"):
        print(f'### ### {file.name}')
        shutil.copyfile(os.path.join(dir_name, file.name), os.path.join(yearbook_dir, prefix + file.name))


dir_name = sys.argv[1]
yearbook_dir = os.path.join(dir_name, 'yearbook')

if not os.path.isdir(yearbook_dir):
    os.mkdir(yearbook_dir)

yearbook(yearbook_dir, dir_name)
