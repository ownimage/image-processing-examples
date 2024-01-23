import sys
import time
from jproperties import Properties

USAGE = ('USAGE: python timestamp_properties.py save_start_time <properties_file_name.properties> <property_name> \n'
         '\n'
         'When used as a script this will open/create the specified <properties_file> and write the current time as a '
         'timestamp in the <property_name> given.\n'
         '\n'
         'When used as an import:\n'
         '    the function get_timestamp(file_name, property_name) will open the file file_name '
         'and return the property property_name.  If either the file or the property do not exist it will return'
         'None.'
         '\n'
         '    the function save_timestamp(file_name, property_name) will save the current timestamp in the file '
         'property_file in the property property_name.  The other properties in the file are not affected, '
         'BUT comments will be.'
         )


def save_timestamp(file_name, property_name):
    p = Properties()
    try:
        with open(file_name, "r+b") as f:
            p.load(f, encoding='utf-8')
    except:
        pass

    p[property_name] = f'{time.time()}'
    with open(file_name, "w+b") as f:
        p.store(f, encoding='utf-8')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(USAGE)
        exit()

    file_name = sys.argv[1]
    property_name = sys.argv[2]

    save_timestamp(file_name, property_name)


def get_timestamp(file_name, property_name):
    try:
        p = Properties()
        with open(file_name, "rb") as f:
            p.load(f, encoding='utf-8')

        v = p[property_name]
        return v.data if v is not None else None
    except:
        return None