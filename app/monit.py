#!/usr/bin/env python
from arguments import argument_management
from logs import write_log_message
from file_handler import create_file, file_exists, get_directory_files
from system_info_collector import (
    get_ram_informations,
    get_cpu_usage,
    get_disk_usage,
    check_tcp_ports,
)
from average import compute_values_average
from json_handler import create_report_file_json, read_json_file
from check_output import system_check_output, average_check_output
from file_info_collector import get_files_values, get_files_from_last_hours
from argparse import ArgumentParser
from uuid import uuid1
from datetime import datetime
from sys import exit


def system_check():
    ram_usage = get_ram_informations()
    disk_usage = get_disk_usage()
    cpu_usage = get_cpu_usage()
    tcp_ports_info = check_tcp_ports()
    (
        check_id,
        check_date,
    ) = uuid1().hex, datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    exit(0)


def list_checks():
    check_files = get_directory_files("/var/monit/")
    if not check_files:
        print("No check file found")
        exit(0)
    check_files_output = "All check files made :\n\n"
    for file in check_files:
        check_files_output += f"  - {file} (located in /var/monit/{file})\n"
    print(check_files_output)

    write_log_message(f"monit.py --list success")
    exit(0)


def get_last_check():
    check_directory = "/var/monit/"
    check_files = get_directory_files(check_directory)

    if not check_files:
        print("No check file found, please make a check to get the last check values")
        exit(1)

    last_check_file_name = check_files[-1]
    last_check_file_path = check_directory + last_check_file_name
    last_check_file = open(last_check_file_path)

    check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info = (
        read_json_file(last_check_file)
    )
    system_check_output(
        check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info
    )
    write_log_message(f"monit.py --get-last success")
    exit(0)


def get_average_check_values(hours):
    check_files_from_last_hours = get_files_from_last_hours(hours)
    last_hours_check_values = get_files_values(check_files_from_last_hours)
    average_check_values = compute_values_average(last_hours_check_values)
    average_check_output(average_check_values)
    write_log_message(f"monit.py --get-avg {hours} success")
    exit(0)


def main():
    parser = ArgumentParser()
    args = argument_management(parser)

    if not file_exists("/etc/monit/monit.conf"):
        create_file("/etc/monit/", "monit.conf", {"tcp_ports": []})

    if args.check is True:
        system_check()
    if args.list is True:
        list_checks()
    if args.get_last is True:
        get_last_check()
    if args.get_avg is not None:
        get_average_check_values(args.get_avg)

    if (
        args.check is False
        and args.list is False
        and args.get_last is False
        and args.get_avg is None
    ):
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()