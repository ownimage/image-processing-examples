import os
import os.path
import sys
from pathlib import Path
import subprocess
import shutil


def refresh(yearbook_dir, dir_name):
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
    data = os.path.join(dir_name, 'data.txt')
    run = os.path.join(dir_name, 'run.lnk')
    refresh = os.path.join(dir_name, 'refresh.cmd')

    if not os.path.exists(refresh):
        shutil.copyfile('refresh.cmd', refresh)

    if os.path.exists(data) and os.path.exists(refresh) and os.path.exists(run):
        refresh_command = f'"{str(refresh)}"'
        result = subprocess.run(refresh_command, cwd=dir_name, shell=True, capture_output=True, text=True)
        print(f'#### {refresh_command}')
        print(result.stdout)
        print(result.stderr)

        run_command = f'"{str(run)}" "{str(data)}"'
        result = subprocess.run(run_command, shell=True, capture_output=True, text=True)
        print(f'#### {run_command}')
        print(result.stdout)
        print(result.stderr)

dir_name = sys.argv[1]
yearbook_dir = os.path.join(dir_name, 'yearbook')

if not os.path.isdir(yearbook_dir):
    os.mkdir(yearbook_dir)

refresh(yearbook_dir, dir_name)
