from constants import (
	DRUGS_FINISH_LINE,
	MINED_OBJECTS_FILE_NAME,
	FILE_MINED_SEPARATOR
)
from utils import split_list, get_file_path


def get_mined_objects():
    proteins = []
    drugs = []
    viruses = []
    with open(get_file_path(MINED_OBJECTS_FILE_NAME), 'r') as file:
        data = file.read().splitlines()
        drugs = split_list(FILE_MINED_SEPARATOR, data[0:DRUGS_FINISH_LINE])
        proteins = split_list(FILE_MINED_SEPARATOR, data[DRUGS_FINISH_LINE:])
    return {
        "drugs": drugs,
        "proteins": proteins,
        "viruses": viruses
    }
