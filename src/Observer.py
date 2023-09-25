import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FILE_SIZE = 20_000_000
DIR_TO_WATCH = "./VideoFile"

verbose = print
# def verbose(x):
#     pass

class DirectoryEventHandler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return

        if event.event_type == 'created':
            # Take any action here when a file is first created.
            verbose('Received created event - ' + event.src_path + '.')

            if os.path.isdir(DIR_TO_WATCH):
                directory_size = sum(os.path.getsize(DIR_TO_WATCH + '/' + f) for f in os.listdir(DIR_TO_WATCH))
                sorted_file_list = sorted([DIR_TO_WATCH + '/' + f for f in os.listdir(DIR_TO_WATCH)], key=os.path.getctime)

                if len(sorted_file_list) > 1:
                    verbose('Finish' + sorted_file_list[-2])

                if directory_size > FILE_SIZE:
                    os.remove(sorted_file_list[0])

            return

        if event.event_type == 'modified':
            pass
            # Taken any action here when a file is modified.
            # print(f"Received modified event - {event.src_path}.")

if __name__ == '__main__':
    observer = Observer()
    event_handler = DirectoryEventHandler()
    observer.schedule(event_handler, DIR_TO_WATCH, recursive=True)
    observer.start()