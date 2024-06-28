import os, sys, csv
from slideshow import create_slide

csv_filename = sys.argv[1]
csv_path = os.path.dirname(csv_filename)


def process_row(row):
    process(os.path.join(csv_path, row[0]), row[1], row[2])


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
