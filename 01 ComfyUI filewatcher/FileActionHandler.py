import logging

from watchdog.events import FileSystemEventHandler

import ComfyUIRunner
from ComfyUIRunner import process_file
from FileUtil import FileUtil


class FileActionHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    def __init__(self, logger=None):
        super().__init__()

        self.logger = logger or logging.root

    def on_moved(self, event):
        super().on_moved(event)

        what = "directory" if event.is_directory else "file"
        src = FileUtil(event.src_path)
        dest = FileUtil(event.dest_path)
        self.logger.info(
            "Moved %s: from %s to %s", what, src.absolute_filename(), dest.absolute_filename()
        )

    def on_created(self, event):
        super().on_created(event)

        what = "directory" if event.is_directory else "file"
        f = FileUtil(event.src_path)
        self.logger.info("Created %s: %s", what, f.absolute_filename())
        ComfyUIRunner.process_file(f.absolute_filename(), f.basename())


    def on_deleted(self, event):
        super().on_deleted(event)

        what = "directory" if event.is_directory else "file"
        f = FileUtil(event.src_path)
        self.logger.info("Deleted %s: %s", what, f.absolute_filename())

    def on_modified(self, event):
        super().on_modified(event)

        what = "directory" if event.is_directory else "file"
        f = FileUtil(event.src_path)
        self.logger.info("Modified %s: %s", what, f.absolute_filename())
