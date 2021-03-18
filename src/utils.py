from pathlib import Path
from constants import FILES_PATH


def split_list(separator, objects):
    new_list = []
    for i in objects:
        new_list.extend(i.split(separator))
    return new_list


def get_file_path(filename):
    files_folder = Path(FILES_PATH)
    return files_folder / filename
