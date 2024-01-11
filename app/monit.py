from argparse import ArgumentParser
from psutil import virtual_memory, disk_usage, cpu_percent
import socket
from contextlib import closing
from json import load, dump
from os.path import isfile, exists
from os import makedirs
from uuid import uuid1
from datetime import datetime
from sys import exit


def argument_management(parser):
    g = parser.add_mutually_exclusive_group()
    
    g.add_argument("-c", "--check", action="store_true", help="inspect RAM, CPU and Disk usage, check if TCP ports specified in config file (/etc/monit/monit.conf) are open and used, output the results and store these in a file located in /var/monit/")
    g.add_argument("-l", "--list", action="store_true", help="output all the check files name and path")
    g.add_argument("--get-last", action="store_true", help="output the last check file results")
    g.add_argument("--get-avg", action="store", type=int, help="output average check values since the last X hours, X is the integer value given in argument")
    
    return parser.parse_args()

def file_exists(file_path):
    if exists(file_path) and isfile(file_path):
        return True
    return False

def create_file(file_directory, file_name, json_data):
    if not exists(file_directory):
        makedirs(file_directory)
    
    with open(f"{file_directory}{file_name}", "w") as conf_file:
        dump(json_data, conf_file)

def get_ram_informations():
    ram = virtual_memory()
    
    total_ram = ram.total
    available_ram = ram.available
    used_ram = ram.used
    free_ram = ram.free
    percent_used = ram.percent
    
    return total_ram, available_ram, used_ram, free_ram, percent_used

def get_disk_usage():
    # try catch maybe ?
    disk = disk_usage('/')
    
    total_disk = disk.total / 1024 / 1024 / 1024
    free_disk = disk.free / 1024 / 1024 / 1024
    used_disk = disk.used / 1024 / 1024 / 1024
    percent_used = disk.percent
    
    return total_disk, free_disk, used_disk, percent_used

def get_cpu_usage():
    return cpu_percent()

def is_port_open(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        socket.setdefaulttimeout(2.0)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            sock.close()
            return True
        else:
            sock.close()
            return False

def check_tcp_ports():
    with open('/etc/monit/monit.conf') as conf_file:
        config = load(conf_file)
    
    ports = config["tcp_ports"]
    print(ports)
    
    ports_checking_report = {}
    for port in ports:
        is_open = is_port_open(port)
        ports_checking_report[str(port)] = is_open
        
    return ports_checking_report

def get_id():
    return uuid1()

def get_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
def create_report_file_json(ram_usage, disk_usage, cpu_usage, tcp_ports_info):
    total_ram, available_ram, used_ram, free_ram, percent_used_ram = ram_usage
    total_disk, free_disk, used_disk, percent_used_disk = disk_usage
    percent_used_cpu = cpu_usage 
    report_json = {
        "id": get_id(),
        "date": get_datetime(),
        "ram": {
            "total_ram": total_ram,
            "available_ram": available_ram,
            "used_ram": used_ram,
            "free_ram": free_ram,
            "percent_used": percent_used_ram
        },
        "disk": {
            "total_disk": total_disk,
            "free_disk": free_disk,
            "used_disk": used_disk,
            "percent_used": percent_used_disk
        },
        "cpu": {
            "percent_used": percent_used_cpu
        }
    }
    if tcp_ports_info != {}:
        report_json["tcp_ports"] = tcp_ports_info
        
    return report_json

def system_check():
    ram_usage = get_ram_informations()
    disk_usage = get_disk_usage()
    cpu_usage = get_cpu_usage()
    tcp_ports_info = check_tcp_ports()
    
    report_file_name = f"monit_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    json_report_file = create_report_file_json(ram_usage, disk_usage, cpu_usage, tcp_ports_info)
    
    system_check_output(ram_usage, disk_usage, cpu_usage, tcp_ports_info)
    create_file("/var/monit/",report_file_name, json_report_file)
    
def system_check_output(ram_usage, disk_usage, cpu_usage, tcp_ports_info):
    total_ram, available_ram, used_ram, free_ram, percent_used_ram = ram_usage
    total_disk, free_disk, used_disk, percent_used_disk = disk_usage
    percent_used_cpu = cpu_usage 
    check_output = f"""
CHECK - {get_id()},

Date: {get_datetime()},

RAM: 
    Total RAM: {total_ram}
    Available RAM: {available_ram}
    Used RAM: {used_ram}
    Free RAM: {free_ram}
    Precent Used: {percent_used_ram} %
    
Disk: 
    Total Disk: {total_disk} GB
    Free Disk: {free_disk} GB
    Used Disk: {used_disk} GB
    Percent Used: {percent_used_disk} %
    
CPU:
    Percent Used: {percent_used_cpu} %\n"""
    if tcp_ports_info != {}:
        ports_output = ""
        for port, status in tcp_ports_info.items():
            ports_output += f"    {port}: {status}\n"
        check_output += f"TCP PORTS:\n{ports_output}"
    
    print(check_output)
    
def list_checks():
    print("list_checks")

def get_last_check():
    print("last_check")

def get_average_check_values():
    print("average_check_values")

def main():
    parser = ArgumentParser()
    args = argument_management(parser)
    
    if not file_exists('/etc/monit/monit.conf'):
        create_file("/etc/monit/", "monit.conf", { "tcp_ports": [] })
        
    if args.check is True:
        system_check()
    if args.list is True:
        list_checks()
    if args.get_last is True:
        get_last_check()
    if args.get_avg is not None:
        get_average_check_values()
        
    if args.check is False and args.list is False and args.get_last is False and args.get_avg is None:
        parser.print_help()
        exit(1)

if __name__ == "__main__":
    main()