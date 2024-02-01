from datetime import datetime, timedelta
from sys import exit as sys
from monit.json_handler import read_json_file
from monit.file_handler import get_directory_files


def get_files_values(files):
    """
    Get all files json_values and return a dict containing RAM, disk and CPU informations from json
    
    Args:
        files: list of check file name
    Returns:
        check_values: dict containing RAM, disk and CPU informations
    """
    check_values = {
        "ram":{"total_ram":[],"available_ram":[],"used_ram":[],"free_ram":[],"percent_used":[]},
        "disk":{"total_disk":[],"free_disk":[],"used_disk":[],"percent_used":[]},"cpu":[] 
    }
    for file in files:
        with open(file, "r", encoding="utf8") as json_file:
            json_file_values = read_json_file(json_file)
        ram_usage, disk_usage, cpu_usage = json_file_values[2], json_file_values[3], json_file_values[4]
        check_values["ram"]["total_ram"].append(ram_usage[0])
        check_values["ram"]["available_ram"].append(ram_usage[1])
        check_values["ram"]["used_ram"].append(ram_usage[2])
        check_values["ram"]["free_ram"].append(ram_usage[3])
        check_values["ram"]["percent_used"].append(ram_usage[4])
        check_values["disk"]["total_disk"].append(disk_usage[0])
        check_values["disk"]["free_disk"].append(disk_usage[1])
        check_values["disk"]["used_disk"].append(disk_usage[2])
        check_values["disk"]["percent_used"].append(disk_usage[3])
        check_values["cpu"].append(cpu_usage)
    return check_values


def get_files_from_last_hours(hours):
    check_directory = "/var/monit/"
    check_files = get_directory_files(check_directory)
    if len(check_files) == 0:
        print("No check file found, please make ")
        sys.exit(1)
    check_files.reverse()

    last_datetime = datetime.now() - timedelta(hours=hours)
    last_datetime = last_datetime.strftime('%Y%m%d%H%M%S')

    check_files_from_last_hours = []
    for file_name in check_files:
        file_date = file_name[6:20]
        if int(file_date) >= int(last_datetime):
            check_files_from_last_hours.append(file_name)

    if len(check_files_from_last_hours) == 0:
        print(f"No check file found in the last {hours} hours")
        sys.exit(1)
    return check_files_from_last_hours
