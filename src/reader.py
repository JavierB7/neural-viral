from constants import (
	DRUGS_FINISH_LINE,
	MINED_OBJECTS_FILE_NAME,
    TRAINING_EXAMPLES_FILE_NAME,
    TRAINING_EXAMPLES_SHORT_FILE_NAME,
	FILE_MINED_SEPARATOR
)
from utils import split_list, get_file_path, get_viruses, clean_list


def get_mined_objects():
    proteins = []
    drugs = []
    viruses = []
    with open(get_file_path(MINED_OBJECTS_FILE_NAME), 'r') as file:
        data = file.read().splitlines()
        drugs = split_list(FILE_MINED_SEPARATOR, data[0:DRUGS_FINISH_LINE])
        proteins = split_list(FILE_MINED_SEPARATOR, data[DRUGS_FINISH_LINE:])
    viruses = get_viruses(proteins)
    proteins = clean_list(proteins, viruses)
    return {
        "drugs": drugs,
        "proteins": proteins,
        "viruses": viruses
    }


def get_examples():
    lines = []
    with open(
        get_file_path(TRAINING_EXAMPLES_FILE_NAME), 
        'r', 
        encoding="utf8") as file:
        for line in file:
            if len(line.split()) == 0:
                continue
            lines.append(line.rstrip())
    return lines
