from uuid import uuid1
from datetime import datetime
import sys
from logs import write_log_message
from file_handler import create_file, get_directory_files
from system_info_collector import (
    get_ram_informations,
    get_cpu_usage,
    get_disk_usage,
    check_tcp_ports,
)
from average import calcultate_averages
from json_handler import create_report_file_json, read_json_file
from check_output import system_check_output, average_check_output
from file_info_collector import get_files_values, get_files_from_last_hours


def system_check():
    ram_usage = get_ram_informations()
    disk_usage = get_disk_usage()
    cpu_usage = get_cpu_usage()
    tcp_ports_info = check_tcp_ports()
    (check_id, check_date) = uuid1().hex, datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_file_name = f"monit_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    json_report_file = create_report_file_json(
        check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info
    )

    system_check_output(
        check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info
    )
    create_file("/var/monit/", report_file_name, json_report_file)
    write_log_message(
        f"monit.py --check success (new check file located in /var/monit/{report_file_name})"
    )
    sys.exit(0)


def list_checks():
    check_files = get_directory_files("/var/monit/")
    if not check_files:
        print("No check file found")
        sys.exit(0)
    check_files_output = "All check files made :\n\n"
    for file in check_files:
        check_files_output += f"  - {file} (located in /var/monit/{file})\n"
    print(check_files_output)

    write_log_message("monit.py --list success")
    sys.exit(0)


def get_last_check():
    check_directory = "/var/monit/"
    check_files = get_directory_files(check_directory)

    if not check_files:
        print("No check file found, please make a check to get the last check values")
        sys.exit(1)

    last_check_file_name = check_files[-1]
    last_check_file_path = check_directory + last_check_file_name
    with open(last_check_file_path, "r", encoding="utf8") as last_check_file:
        check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info = (
            read_json_file(last_check_file)
        )
    system_check_output(
        check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info
    )
    write_log_message("monit.py --get-last success")
    sys.exit(0)


def get_average_check_values(hours):
    check_files_from_last_hours = get_files_from_last_hours(hours)
    last_hours_check_values = get_files_values(check_files_from_last_hours)
    average_check_values = calcultate_averages(last_hours_check_values)
    average_check_output(average_check_values)
    write_log_message(f"monit.py --get-avg {hours} success")
    sys.exit(0)
