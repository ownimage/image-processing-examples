import os.path
from pathlib import Path


class FileUtil:
    def __init__(self, filename):
        self._filename = filename
        self._extension = os.path.splitext(self._filename)[1][1:]
        self._basename = Path(self._filename).stem
        self._absoluteFilename = os.path.abspath(self._filename)

    def filename(self):
        return self._filename

    def extension(self):
        return self._extension

    def basename(self):
        return self._basename

    def absolute_filename(self):
        return self._absoluteFilename


