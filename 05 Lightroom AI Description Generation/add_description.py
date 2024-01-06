import os
import pathlib
import sys

dir_path = sys.argv[1]
paths = []

for path in os.listdir(dir_path):
    file = os.path.join(dir_path, path)
    if os.path.isfile(file) and path != 'rename.txt':
        path = pathlib.Path(path)
        paths.append(path)

zeros = len(f'{len(paths)}')

for index, path in enumerate(paths):
    old_name = os.path.join(dir_path, path)
    new_name = os.path.join(dir_path, f'{index:0{zeros}d}{path.suffix}')
    print(f'rename {old_name} to {new_name}')
    os.rename(old_name, new_name)
