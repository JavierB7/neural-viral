from pathlib import Path
from constants import FILES_PATH


def split_list(separator, objects):
    new_list = []
    for i in objects:
        separated = i.split(separator)
        new_list.extend([element.rstrip() for element in separated])
    return new_list


def get_file_path(filename):
    files_folder = Path(FILES_PATH)
    return files_folder / filename


def get_viruses(objects):
    an_iterator = filter(lambda word: word.find("SARS") != -1, objects)
    return list(an_iterator)


def clean_list(list_to_update, list_to_be_removed):
    return [x for x in list_to_update if x not in list_to_be_removed]
    
