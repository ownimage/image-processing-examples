import os, sys, csv
from pathlib import Path

from slideshow import create_slide

csv_filename = sys.argv[1]
csv_path = os.path.dirname(csv_filename)

print(f'{csv_path}')
date_dir = os.path.split(os.path.split(Path(csv_path))[0])[1]
print(f'{date_dir}')
default_date = date_dir[0:4] + ' ' + date_dir[4:6] + ' ' + date_dir[6:8]
default_title = date_dir[9:].strip(' -_')
print(f'date = {default_date} \ntitle = "{default_title}"')


def process_row(row):
    date = ''
    if len(row) > 2:
        date = row[1]
    if len(date) == 0:
        date = default_date

    title = ''
    if len(row) >= 3:
        title = row[2]
    if len(title) == 0:
        title = default_title

    process(os.path.join(csv_path, row[0]), date, title)


def process(filename, date, title):
    print(f'filename={filename}, title={title}, date={date}')
    create_slide(filename, title, date)


with open(csv_filename, 'r') as csv_file:
    reader = csv.reader(csv_file)

    header_read = False
    for row in reader:
        if header_read:
            process_row(row)
        header_read = True
