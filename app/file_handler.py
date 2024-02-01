from os.path import isfile, exists
from os import makedirs, listdir
from json import dump


def file_exists(file_path):
    if exists(file_path) and isfile(file_path):
        return True
    return False


def create_file(file_directory, file_name, json_data):
    if not exists(file_directory):
        makedirs(file_directory)

    with open(f"{file_directory}{file_name}", "w", encoding='utf-8') as conf_file:
        dump(json_data, conf_file, separators=(",", ":"))


def get_directory_files(directory):
    return [f for f in listdir(directory) if isfile(directory + f)]
